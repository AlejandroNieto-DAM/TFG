package com.example.pruebaclientsocket;

import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class SocketThread implements Runnable {

    public static final int BUFFER_SIZE = 2048;
    private PrintWriter out = null;
    private BufferedReader in = null;

    @Override
    public void run() {
        Socket a = null;
        try {
            a = new Socket("192.168.1.137", 1234);
        } catch (IOException e) {
            e.printStackTrace();
        }

        try {
            out = new PrintWriter(a.getOutputStream());
            in = new BufferedReader(new InputStreamReader(a.getInputStream()));
        } catch (IOException e) {
            e.printStackTrace();
        }

        out.write("yeyo");
        out.flush();




        String message = "";
        int charsRead = 0;
       // char[] buffer = new char[BUFFER_SIZE];

        Log.i("Fuera --> ", "enviao");

        try {

            while((message = in.readLine()) != ""){
                Log.i("Msg --> ", message);
            }

        } catch (IOException e) {
            e.printStackTrace();
            Log.i("Exp --> ", e.toString());
        }

    }
}
