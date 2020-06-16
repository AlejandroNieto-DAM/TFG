package com.example.pruebaandroidclient;

import android.content.Context;
import android.os.AsyncTask;
import android.util.Base64;
import android.util.Log;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
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
    private ArrayList<Device> allDevices;
    private LoggedActivity myLoggedActivity;
    private Socket socket;
    private boolean finished = false;
    private byte[] outBytes;
    private Boolean firstTimePassed;
    private int getImagesIndex;
    private String thread_owner;
    private boolean loginSuccess;

    /**
     * @brief Constructor
     * @param mainActivity which is the mainactivity in which this class has been instanciated
     */
    public ClientThread(MainActivity mainActivity)  {
        out = null;
        in = null;
        this.mainActivity = mainActivity;
        this.myProtocol = new ClientProtocol(this);
        thread_owner = "";
        getImagesIndex = 0;
        firstTimePassed = false;
        loginSuccess = false;
    }

    /**
     * @brief Start the socket connection and start to listen to the server
     * @pre The server has to be up to get connected with this socket
     * @post This app will be listening to the socket and with the possibility to send data to the server
     */
    @Override
    protected Void doInBackground(Void... voids) {
        String message;

        socket = null;
        try {
            socket = new Socket("192.168.1.107", 1235);
        } catch (IOException e) {
            e.printStackTrace();
            Log.i("[EXCEPTION] " , e.toString());
        }

        try {
            out = new PrintWriter(socket.getOutputStream());
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        } catch (IOException e) {
            Log.i("[EXCEPTION] " , e.toString());

        }

        try {

            while((message = in.readLine()) != null && !finished){
                Log.i("Msg --> ", message);
                this.processProtocol(message);

            }

        } catch (IOException e) {
            e.printStackTrace();
            Log.i("Exp --> ", e.toString());
        }


        return null;
    }


    /**
     * @brief procces the message received by the server to see if it have all the conditions to know if the message is real
     * @param message is the message received by the server
     * @pre the socket has to been connected
     * @throws IOException
     */
    public void processProtocol(String message) throws IOException {
        if(message.contains("PROTOCOLTFG")){
            if(message.contains("SERVERTFG")){
                if(message.contains("TOTAL")) {

                    this.receiveDevices(message);

                } else if (message.contains("TRYOPENINGDEVICE")){
                    this.deviceIsInAction(message);
                } else if (message.contains("TRYCLOSINGDEVICE")){
                    this.deviceIsInAction(message);
                } else if (message.contains("OPENINGDEVICE")){

                    this.refreshOpenDoor(message);

                } else if (message.contains("CLOSINGDEVICE")){

                    this.refreshCloseDoor(message);

                } else if (message.contains("PHOTO")){

                    this.processPhoto(message);

                } else if (message.contains(("FINIMAGE"))){

                    this.finImage(message);

                } else if (message.contains(("ERROR"))){

                    if(!loginSuccess){
                        this.mainActivity.loadToastMsg();
                    } else {
                        this.myLoggedActivity.loadToastMsg();
                    }

                }
            }
        }

    }


    public void deviceIsInAction(String message){
        String[] datos = message.split("#");

        for(Device d : allDevices){
            if(d.getId() == Integer.parseInt(datos[4])){
                d.setState(2);
            }
        }

        this.myLoggedActivity.refresh(allDevices);
    }

    /**
     * @brief Process the devices received to load it in one array and generates the protocol to get the first device image
     * @param message which is the message received by the server with all the devices
     * @pre the socket has to been connected
     */
    public void receiveDevices(String message){
        allDevices = myProtocol.proccesDevices(message);
        if(allDevices.size() > 0){
            String output = this.myProtocol.getPhoto(this.allDevices.get(getImagesIndex).getId());
            this.sendMsg(output);
        }

    }

    /**
     * @brief Process the message of the server that says that one door was opened
     * @param message which is the message received by the server with the id of the opened device
     * @pre the socket has to been connected
     * @post the data of the recycler view in the LoggedActivity will be updated with the new value
     */
    public void refreshOpenDoor(String message){
        String[] datos = message.split("#");

        for(Device d : allDevices){
            if(d.getId() == Integer.parseInt(datos[4])){
                d.setState(1);
            }
        }

        this.myLoggedActivity.refresh(allDevices);
    }

    /**
     * @brief Process the message of the server that says that one door was closed
     * @param message which is the message received by the server with the id of the closed device
     * @pre the socket has to been connected
     * @post the data of the recycler view in the LoggedActivity will be updated with the new value
     */
    public void refreshCloseDoor(String message){
        String[] datos = message.split("#");

        for(Device d : allDevices){
            if(d.getId() == Integer.parseInt(datos[4])){
                d.setState(0);
            }
        }

        this.myLoggedActivity.refresh(allDevices);
    }

    /**
     * @brief Process the message received by the server with 512 bytes of the photo and ads it to the previous bytes.
     * @param message is the message received by the server in which there are 512 bytes of the photo
     * @pre the socket has to been connected
     * @post one photo will be formed with all the bytes
     * @throws IOException
     */
    public void processPhoto(String message) throws IOException {
        String[] datos = message.split("#");
        byte[] data = Base64.decode(datos[4].substring(2, datos[4].lastIndexOf("\'")), Base64.DEFAULT);

        ByteArrayOutputStream output = new ByteArrayOutputStream();

        if(firstTimePassed){
            output.write(outBytes);
            output.write(data);
        } else {
            output.write(data);
            firstTimePassed = true;
        }


        outBytes = output.toByteArray();
    }

    /**
     * @brief Forms a image with the bytes previous received and if there is more devices to get their photo arms the protocol to send the msg to the server
     * @param message which is the message received by the server in which says that the image dont have more bytes.
     * @pre the socket has to been connected
     * @post the image finished will be set on the corresponding device
     */
    public void finImage(String message){

        if(getImagesIndex == this.allDevices.size() - 1){

            this.allDevices.get(getImagesIndex).setImage(outBytes);
            this.mainActivity.startLoggedActivity(allDevices);
            this.loginSuccess = true;

        } else {
            this.allDevices.get(getImagesIndex).setImage(outBytes);
            this.getImagesIndex++;
            ByteArrayOutputStream output = new ByteArrayOutputStream();
            output.reset();
            outBytes = output.toByteArray();
            String send = this.myProtocol.getPhoto(this.allDevices.get(getImagesIndex).getId());
            this.sendMsg(send);

        }

    }

    /**
     * @brief Is the method called to stop this thread
     * @pre the socket has to been connected
     * @post this thread will be stopped
     */
    public void setFinished() {
        this.finished = true;
        this.sendMsg(this.myProtocol.sendLogout());
    }

    /**
     * @return Returns all the devices
     */
    public ArrayList getAllDevices(){
        return this.allDevices;
    }

    /**
     * @brief Set the loggedActivity to this class
     * @param myLoggedActivity which is the second activity
     * @pre The login has to been sucessful
     */
    public void setMyLoggedActivity(LoggedActivity myLoggedActivity){
        this.myLoggedActivity = myLoggedActivity;
    }

    /**
     * @brief Sends to the server the message with the protocol to try to get logged
     * @param login is the login of the user who wants to get logged
     * @param password which is the password of the user who wants to get logged
     * @pre the socket has to been connected
     * @post if the login is successful the apps goes to the next application
     */
    public void sendLogin(String login, String password){
        this.thread_owner = login;
        String output = this.myProtocol.sendLogin(login, password);
        this.sendMsg(output);
    }

    /**
     * @return Returns the thread_owner
     */
    public String getThreadOwner(){
        return this.thread_owner;
    }

    /**
     * @brief Sends the param msg by the socket to the server
     * @param msg is the msg that will be sent to the server
     * @pre the socket has to been connected
     * @post the server will return an answer
     */
    private void sendMsg(String msg){
        out.write(msg);
        out.flush();
    }

    /**
     * @brief Send the message to open a specific device to the server
     * @param id which is the id of the device we want to open
     * @pre the socket has to been connected
     * @post if its possible the specific device will be opened
     */
    public void sendOpenDevice(int id){
        String output = this.myProtocol.sendOpenDevice(id);
       this.sendMsg(output);
    }

    /**
     * @brief Send the message to close a specific device to the server
     * @param id which is the id of the device we want to close
     * @pre the socket has to been connected
     * @post if its possible the specific device will be closed
     */
    public void sendCloseDevice(int id){
        String output = this.myProtocol.sendCloseDevice(id);
        this.sendMsg(output);
    }

}
