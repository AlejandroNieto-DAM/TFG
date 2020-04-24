package com.example.pruebaandroidclient;

public class Door {
    int id = 0;
    String identifier_name;
    int state;
    int maintenance;
    String urlphoto;

    public Door (int id, String identifier_name, int state, int maintenance, String urlphoto){
        this.id = id;
        this.identifier_name = identifier_name;
        this.state = state;
        this.maintenance = maintenance;
        this.urlphoto = urlphoto;
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

    public String getUrlphoto(){
        return this.urlphoto;
    }

}
