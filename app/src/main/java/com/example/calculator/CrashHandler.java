package com.example.calculator;

import android.content.Context;
import android.os.Environment;

import java.io.File;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;

public class CrashHandler implements Thread.UncaughtExceptionHandler {
    private final Context context;
    private final Thread.UncaughtExceptionHandler defaultHandler;

    public CrashHandler(Context ctx) {
        context = ctx.getApplicationContext();
        defaultHandler = Thread.getDefaultUncaughtExceptionHandler();
    }

    @Override
    public void uncaughtException(Thread t, Throwable e) {
        try {
            File dir = getStorageDir();
            if (!dir.exists()) dir.mkdirs();
            File file = new File(dir, "crash_" + System.currentTimeMillis() + ".log");
            FileOutputStream fos = new FileOutputStream(file);
            PrintWriter pw = new PrintWriter(new OutputStreamWriter(fos));
            e.printStackTrace(pw);
            pw.flush();
            pw.close();
            fos.close();
        } catch (Throwable ignore) {
        }

        if (defaultHandler != null) {
            defaultHandler.uncaughtException(t, e);
        } else {
            System.exit(2);
        }
    }

    private File getStorageDir() {
        try {
            if (Environment.MEDIA_MOUNTED.equals(Environment.getExternalStorageState())) {
                File ext = context.getExternalFilesDir(null);
                if (ext != null) return ext;
            }
        } catch (Exception ignored) {}
        return context.getFilesDir();
    }
}
