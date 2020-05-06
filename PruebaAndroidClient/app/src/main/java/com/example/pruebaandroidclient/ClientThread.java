package com.example.pruebaandroidclient;

import android.content.Context;
import android.content.ContextWrapper;
import android.graphics.Bitmap;
import android.os.AsyncTask;
import android.os.Environment;
import android.util.Base64;
import android.util.Log;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.io.Serializable;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Random;

public class ClientThread extends AsyncTask<Void, Void, Void> {

    private PrintWriter out;
    private BufferedReader in;
    private MainActivity mainActivity;
    private ClientProtocol myProtocol;
    private ArrayList<Door> allDoors;
    private LoggedActivityEx myLoggedActivity;
    private Context context;
    Socket a;
    public boolean finished = false;

    public ClientThread(MainActivity mainActivity, Context context)  {
        out = null;
        in = null;
        this.mainActivity = mainActivity;
        this.myProtocol = new ClientProtocol();
        this.context = context;
        Log.i("Creada task " , "yeyo");
    }

    @Override
    protected Void doInBackground(Void... voids) {
        String message;

        a = null;
        try {
            a = new Socket("192.168.1.133", 12345);
        } catch (IOException e) {
            e.printStackTrace();
            Log.i("[EXCEPTION] " , e.toString());
        }

        try {
            out = new PrintWriter(a.getOutputStream());
            in = new BufferedReader(new InputStreamReader(a.getInputStream()));
            Log.i("Por aqui hemos pasao", "yeye");
        } catch (IOException e) {
            Log.i("[EXCEPTION] " , e.toString());

        }

        try {

            while((message = in.readLine()) != null){
                Log.i("Msg --> ", message);
                Log.i("Finished --> ", String.valueOf(finished));

                if(message.contains("TOTAL")){
                    allDoors = myProtocol.proccesDoors(message);
                    this.mainActivity.startLoggedActivity(allDoors);

                } else if (message.contains("OPENINGDOOR")){

                    String[] datos = message.split("#");

                    for(Door d : allDoors){
                        if(d.getId() == Integer.parseInt(datos[2])){
                            d.setState(1);
                        }
                    }

                    this.myLoggedActivity.refresh(allDoors);

                } else if (message.contains("CLOSINGDOOR")){

                    String[] datos = message.split("#");

                    for(Door d : allDoors){
                        if(d.getId() == Integer.parseInt(datos[2])){
                            d.setState(0);
                        }
                    }

                    this.myLoggedActivity.refresh(allDoors);

                }


            }

            Log.i("Hemos salio=", "o no =?");

        } catch (IOException e) {
            e.printStackTrace();
            Log.i("Exp --> ", e.toString());
        }


        return null;
    }


    public void setFinished(boolean finished) {

        this.finished = finished;
        Log.i("Finished", String.valueOf(finished));
    }

    public ArrayList getAllDoors(){
        return this.allDoors;
    }

    public void setMyLoggedActivity(LoggedActivityEx myLoggedActivity){
        this.myLoggedActivity = myLoggedActivity;
    }


    public void sendLogin(String login, String password){
        String output = "PROTOCOLTFG#CLIENT#FECHA#LOGIN#" + login + "#" + password + "#END";
        sendMsg(output);

    }

    private void sendMsg(String msg){
        out.write(msg);
        out.flush();
    }

    public void sendOpenDoor(int id){
        String output = "PROTOCOLTFG#CLIENT#FECHA#OPENDOOR#" + String.valueOf(id) + "#END";
        sendMsg(output);
    }

    public void sendCloseDoor(int id){
        String output = "PROTOCOLTFG#CLIENT#FECHA#CLOSEDOOR#" + String.valueOf(id) + "#END";
        sendMsg(output);
    }

}
