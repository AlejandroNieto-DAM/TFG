package com.example.pruebaandroidclient;

import android.os.AsyncTask;
import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.ArrayList;

public class ClientThread extends AsyncTask<Void, Void, Void> {

    private PrintWriter out;
    private BufferedReader in;
    private MainActivity mainActivity;
    private ClientProtocol myProtocol;
    private ArrayList<Door> allDoors;

    public ClientThread(MainActivity mainActivity){
        out = null;
        in = null;
        this.mainActivity = mainActivity;
        this.myProtocol = new ClientProtocol();
    }


    @Override
    protected Void doInBackground(Void... voids) {

        Socket a = null;
        try {
            a = new Socket("192.168.1.134", 1234);
        } catch (IOException e) {
            e.printStackTrace();
        }

        try {
            out = new PrintWriter(a.getOutputStream());
            in = new BufferedReader(new InputStreamReader(a.getInputStream()));
        } catch (IOException e) {
            e.printStackTrace();
        }

        String message;

        try {

            while((message = in.readLine()) != null){
                Log.i("Msg --> ", message);

                if(message.contains("TOTAL")){
                    allDoors = myProtocol.proccesDoors(message);
                    this.mainActivity.startLoggedActivity(allDoors);
                }

            }

        } catch (IOException e) {
            e.printStackTrace();
            Log.i("Exp --> ", e.toString());
        }


        return null;
    }

    public void sendLogin(String login, String password){
        String output = "PROTOCOLTFG#CLIENT#FECHA#LOGIN#" + login + "#" + password + "#END";
        sendMsg(output);

    }

    private void sendMsg(String msg){
        out.write(msg);
        out.flush();
    }
}
