import asyncio
import hashlib
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import aiohttp
from tqdm.asyncio import tqdm


async def get_file_size(session, url):
    async with session.head(url) as response:
        if response.status == 200:
            return int(response.headers.get('Content-Length', 0))
    return 0


async def download_chunk(session, url, start, end, filename, pbar=None):
    headers = {'Range': f'bytes={start}-{end}'}
    try:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            with open(filename, 'r+b') as f:
                f.seek(start)
                async for chunk in response.content.iter_chunked(8192):
                    f.write(chunk)
                    if pbar:
                        pbar.update(len(chunk))
    except Exception as e:
        # Retry or handle error
        print(f"Error downloading chunk {start}-{end}: {e}")
        raise


async def download_file(url: str, output_path: str, max_concurrency: int = 4):
    """
    Download file using aiohttp with concurrent chunks.
    """
    output_path = Path(output_path)
    # Create empty file
    with open(output_path, 'wb') as f:
        pass

    async with aiohttp.ClientSession() as session:
        file_size = await get_file_size(session, url)
        if file_size == 0:  # Fallback to single connection if size unknown
            print("Unknown file size, downloading in single stream...")
            async with session.get(url) as response:
                response.raise_for_status()
                with open(output_path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(8192):
                        f.write(chunk)
            return

        # Resize file to target size
        with open(output_path, 'wb') as f:
            f.truncate(file_size)

        chunk_size = file_size // max_concurrency
        tasks = []
        with tqdm(
            total=file_size, unit='B', unit_scale=True, desc=output_path.name
        ) as pbar:
            for i in range(max_concurrency):
                start = i * chunk_size
                end = (
                    start + chunk_size - 1
                    if i < max_concurrency - 1
                    else file_size - 1
                )
                task = download_chunk(
                    session,
                    url,
                    start,
                    end,
                    output_path,
                    pbar,
                )
                tasks.append(task)

            await asyncio.gather(*tasks)


def compute_sha256(file_path):
    """Compute SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192 * 1024), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


async def verify_file_async(file_path: str, expected_hash: str = None):
    """
    Verify file integrity using multiprocessing for hashing.
    """
    loop = asyncio.get_running_loop()

    # Offload hashing to a separate process to avoid blocking the event loop
    with ProcessPoolExecutor() as pool:
        file_hash = await loop.run_in_executor(pool, compute_sha256, file_path)

    is_valid = (
        file_hash.lower() == expected_hash.lower() if expected_hash else None
    )
    return file_hash, is_valid
