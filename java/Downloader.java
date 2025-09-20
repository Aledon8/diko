import java.io.*;
import java.net.*;
import java.nio.file.*;

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
            int fileSize = connection.getContentLength();

            InputStream input = connection.getInputStream();
            FileOutputStream output = new FileOutputStream(outFile);

            byte[] buffer = new byte[8192]; // 8 KB буфер
            int bytesRead;
            long totalRead = 0;
            long startTime = System.currentTimeMillis();

            while ((bytesRead = input.read(buffer)) != -1) {
                output.write(buffer, 0, bytesRead);
                totalRead += bytesRead;

                if (fileSize > 0) {
                    int percent = (int) (totalRead * 100 / fileSize);
                    double mbRead = totalRead / (1024.0 * 1024.0);
                    double mbTotal = fileSize / (1024.0 * 1024.0);

                    long elapsed = System.currentTimeMillis() - startTime;
                    double speed = (totalRead / 1024.0 / 1024.0) / (elapsed / 1000.0); // MB/s

                    System.out.printf("\rDownloading: %d%%  %.2fMB / %.2fMB  [%.2f MB/s]",
                            percent, mbRead, mbTotal, speed);
                }
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
