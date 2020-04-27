package com.example.pruebaandroidclient;

import android.os.Bundle;
import android.os.Parcel;
import android.os.Parcelable;
import android.util.Log;

public class Door implements Parcelable {
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

    protected Door(Parcel in) {
        id = in.readInt();
        identifier_name = in.readString();
        state = in.readInt();
        maintenance = in.readInt();
        urlphoto = in.readString();
    }

    public static final Creator<Door> CREATOR = new Creator<Door>() {
        @Override
        public Door createFromParcel(Parcel in) {
            return new Door(in);
        }

        @Override
        public Door[] newArray(int size) {
            return new Door[size];
        }
    };

    public void setState(int state) {
        this.state = state;
    }

    public void setUrlphoto(String urlphoto) {
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

    public void printDoor(){
        Log.i("Door -> ", id + " " + identifier_name + " " + state + " " + maintenance);
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeInt(id);
        dest.writeString(identifier_name);
        dest.writeInt(state);
        dest.writeInt(maintenance);
        dest.writeString(urlphoto);
    }
}

