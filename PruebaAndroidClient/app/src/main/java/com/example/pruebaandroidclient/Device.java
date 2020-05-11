package com.example.pruebaandroidclient;

import android.util.Log;

public class Device {

    private int id;
    private String identifier_name;
    private int state;
    private int maintenance;
    private byte[] image;

    //Constructor
    public Device(int id, String identifier_name, int state, int maintenance){
        this.id = id;
        this.identifier_name = identifier_name;
        this.state = state;
        this.maintenance = maintenance;
    }

    //Set the byte[] as the actual image
    public void setImage(byte[] image) {
        this.image = image;
    }

    //Set the state as the actual state
    public void setState(int state) {
        this.state = state;
    }

    //Get the id of the Device
    public int getId(){
        return this.id;
    }

    //Get the identifier_name of the Device
    public String getIdentifier_name(){
        return this.identifier_name;
    }

    //Get the state of the Device
    public int getState(){
        return this.state;
    }

    //Get the image of the Device
    public byte[] getImage(){
        return image;
    }
}

