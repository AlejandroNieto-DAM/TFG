package com.example.pruebaandroidclient;

import android.graphics.Bitmap;
import android.os.AsyncTask;
import android.os.Environment;
import android.util.Log;

import java.io.BufferedReader;
import java.io.File;
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

    public ClientThread(MainActivity mainActivity)  {
        out = null;
        in = null;
        this.mainActivity = mainActivity;
        this.myProtocol = new ClientProtocol();
    }


    @Override
    protected Void doInBackground(Void... voids) {

        Socket a = null;
        try {
            a = new Socket("192.168.1.133", 1234);
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
                } else if (message.contains("OPENINGDOOR")){
                    for(Door d : allDoors){
                        if(d.getId() == 1){
                            d.setState(1);
                        }
                    }

                    this.myLoggedActivity.refresh(allDoors);

                } else if (message.contains("CLOSINGDOOR")){
                    for(Door d : allDoors){
                        if(d.getId() == 1){
                            d.setState(0);
                        }
                    }

                    this.myLoggedActivity.refresh(allDoors);
                }

            }

        } catch (IOException e) {
            e.printStackTrace();
            Log.i("Exp --> ", e.toString());
        }


        return null;
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

    private void SaveImage(Bitmap finalBitmap) {

        String root = Environment.getExternalStorageDirectory().toString();
        File myDir = new File(root + "/saved_images");
        if (!myDir.exists()) {
            myDir.mkdirs();
        }
        Random generator = new Random();
        int n = 10000;
        n = generator.nextInt(n);
        String fname = "Image-"+ n +".jpg";
        File file = new File (myDir, fname);
        if (file.exists ())
            file.delete ();
        try {
            FileOutputStream out = new FileOutputStream(file);
            finalBitmap.compress(Bitmap.CompressFormat.JPEG, 90, out);
            out.flush();
            out.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
