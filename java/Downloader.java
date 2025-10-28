import java.io.*;
import java.net.*;

public class Downloader {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: java Downloader <url> <outfile>");
            System.exit(1);
        }

        String urlStr = args[0];
        String outFile = args[1];

        try {
            URL url = new URL(urlStr);
            URLConnection connection = url.openConnection();
            long fileSize = connection.getContentLengthLong(); // может быть -1

            InputStream input = connection.getInputStream();
            FileOutputStream output = new FileOutputStream(outFile);

            byte[] buffer = new byte[8192]; // 8 KB буфер
            int bytesRead;
            long totalRead = 0;
            long startTime = System.currentTimeMillis();

            while ((bytesRead = input.read(buffer)) != -1) {
                output.write(buffer, 0, bytesRead);
                totalRead += bytesRead;

                long elapsed = System.currentTimeMillis() - startTime;
                double mbRead = totalRead / (1024.0 * 1024.0);
                double speed = (totalRead / 1024.0 / 1024.0) / (elapsed / 1000.0); // MB/s

                if (fileSize > 0) {
                    double mbTotal = fileSize / (1024.0 * 1024.0);
                    int percent = (int) (totalRead * 100 / fileSize);

                    System.out.printf(
                        "\rDownloading: %3d%%  %.2fMB / %.2fMB  [%.2f MB/s]",
                        percent, mbRead, mbTotal, speed
                    );
                } else {
                    // fallback — сервер не сообщил размер
                    System.out.printf(
                        "\rDownloading: %.2fMB  [%.2f MB/s]",
                        mbRead, speed
                    );
                }
                System.out.flush();
            }

            input.close();
            output.close();

            System.out.println("\n✅ Download finished: " + outFile);

        } catch (Exception e) {
            System.out.println("❌ Error: " + e.getMessage());
            System.exit(1);
        }
    }
}
