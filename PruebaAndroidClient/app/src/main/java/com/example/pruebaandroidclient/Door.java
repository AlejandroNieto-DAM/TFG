package com.example.pruebaandroidclient;

public class Door {
    int id = 0;
    String identifier_name;
    int state;
    int maintenance;

    public Door (int id, String identifier_name, int state, int maintenance){
        this.id = id;
        this.identifier_name = identifier_name;
        this.state = state;
        this.maintenance = maintenance;
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

}
