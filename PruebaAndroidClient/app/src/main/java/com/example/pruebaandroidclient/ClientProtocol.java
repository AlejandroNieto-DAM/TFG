package com.example.pruebaandroidclient;

import android.util.Log;

import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.ArrayList;

public class ClientProtocol {

    private ClientThread clientThread;

    /**
     * @brief Constructor
     * @param clientThread
     */
    public ClientProtocol(ClientThread clientThread){
        this.clientThread = clientThread;
    }

    /**
     * @brief Get the current time.
     * @return the current time.
     */
    public String getDateTime(){
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        Timestamp timestamp = new Timestamp(System.currentTimeMillis());
        return sdf.format(timestamp);
    }

    /**
     * @brief Compounds the protocol to open a device with its id
     * @param id which is the id of the device we want to open
     * @return Returns the protocol to open a device
     */
    public String sendOpenDevice(int id){
        String output = "PROTOCOLTFG#" + this.getDateTime() + "#CLIENT#ANDROID#" + this.clientThread.getThreadOwner() + "#OPENDEVICE#" + id + "#END";
        return output;
    }

    /**
     * @brief Compounds the protocol to close a device with its id
     * @param id which is the id of the device we want to close
     * @return Returns the protocol to close a device
     */
    public String sendCloseDevice(int id){
        String output = "PROTOCOLTFG#" + this.getDateTime() + "#CLIENT#ANDROID#" + this.clientThread.getThreadOwner() + "#CLOSEDEVICE#" + id + "#END";
        return output;
    }

    /**
     * @brief Compounds the protocol to try to get logged into the application
     * @param login which is the login of the person who wants to get logged
     * @param password which is the password of the user who wants to get logged
     * @return Returns the protocol to try to get logged
     */
    public String sendLogin(String login, String password){
        String output = "PROTOCOLTFG#" + this.getDateTime() + "#CLIENT#ANDROID#LOGIN#" + login + "#" + password + "#END";
        return output;
    }

    /**
     * @brief Compounds the protocol to get logout into the application
     * @pre The user has to been logged previously
     * @return Returns the protocol to get logout
     */
    public String sendLogout(){
        String output = "PROTOCOLTFG#" + this.getDateTime() + "#CLIENT#ANDROID#LOGOUT#" + this.clientThread.getThreadOwner() + "#END";
        return output;
    }

    /**
     * @brief Compounds the protocol to get the photo of one device
     * @param id which is the id of the device we want to get the photo
     * @return Returns the protocol to get the device photo
     */
    public String getPhoto(int id){
        String output = "PROTOCOLTFG#" + this.getDateTime() + "#CLIENT#ANDROID#" + this.clientThread.getThreadOwner() + "#GETPHOTO#" + id + "#END";
        return output;
    }

    /**
     * @brief Proccess all the devices received by the server to display the information in the recycler view of the LoggedActivity
     * @pre The login has to been successful
     * @param inputline which is the data received from server with all the devices information
     * @return Returns one arraylist with the objects of the information received.
     */
    public ArrayList proccesDevices(String inputline){
        ArrayList<Device> devices = new ArrayList<>();

        String[] splitted_devices = inputline.substring(inputline.indexOf("DEVICE")).split("#");

        int index = 0;
        int id_device = 0;
        String door_name = "";
        int state = 0;
        int maintenance = 0;
        for(String s: splitted_devices){

            if(index == 1){
                id_device = Integer.parseInt(s);
            }

            if(index == 2){
                door_name = s;
            }

            if(index == 3){
                state = Integer.parseInt(s);
            }

            if(index == 4){
                maintenance = Integer.parseInt(s);
            }

            if((s.equals("DEVICE") || s.equals("END")) && index >= 4 ){
                index = 0;
                Log.i("Mira una door -->", id_device + " "  + door_name  + " "  + state  + " "  +  maintenance);
                Device auxiliar = new Device(id_device, door_name, state, maintenance);
                devices.add(auxiliar);
                id_device = 0;
                door_name = "";
                state = 0;
                maintenance = 0;
            }
            index++;
        }

        return devices;
    }

}
