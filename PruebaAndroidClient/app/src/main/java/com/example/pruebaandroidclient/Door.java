package com.example.pruebaandroidclient;

import android.util.Log;

public class Door {
    int id = 0;
    String identifier_name;
    int state;
    int maintenance;
    String url;

    public Door (int id, String identifier_name, int state, int maintenance){
        this.id = id;
        this.identifier_name = identifier_name;
        this.state = state;
        this.maintenance = maintenance;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getUrl() {
        return url;
    }

    public void setState(int state) {
        this.state = state;
    }

    public int getId(){
        return this.id;
    }

    public String getIdentifier_name(){
        return this.identifier_name;
    }

    public int getState(){
        return this.state;
    }

    public int getMaintenance(){
        return this.maintenance;
    }

    public void printDoor(){
        Log.i("Door -> ", id + " " + identifier_name + " " + state + " " + maintenance);
    }

}

