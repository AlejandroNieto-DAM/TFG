package com.example.pruebaandroidclient;

import androidx.appcompat.app.AppCompatActivity;
import androidx.constraintlayout.widget.ConstraintLayout;

import android.content.Intent;
import android.os.Bundle;
import android.os.StrictMode;
import android.util.Log;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import java.io.Serializable;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity{

    TextView login;
    TextView passwd;
    Button btnSend;
    ImageView minimap;

    ConstraintLayout ct;
    Boolean clickedTextField = false;
    ClientThread myThread;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        StrictMode.ThreadPolicy policy = new
                StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        login = findViewById(R.id.editText);
        passwd = findViewById(R.id.editText3);
        btnSend = findViewById(R.id.button);
        minimap = findViewById(R.id.imageView3);
        ct = findViewById(R.id.yeyo);

        myThread = new ClientThread(this);
        myThread.execute();



        btnSend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                checkLogin();

            }
        });

        login.setOnFocusChangeListener(new View.OnFocusChangeListener() {
            @Override
            public void onFocusChange(View v, boolean hasFocus) {
                if(!hasFocus){
                    hideKeyboard(v);
                } else {
                    if(clickedTextField == false) {
                        ct.scrollBy(ct.getScrollX(), ct.getScrollY() + 500);
                        clickedTextField = true;
                    }
                }
            }
        });

        passwd.setOnFocusChangeListener(new View.OnFocusChangeListener() {
            @Override
            public void onFocusChange(View v, boolean hasFocus) {
                if(!hasFocus){
                    hideKeyboard(v);
                }  else {
                    if(clickedTextField == false) {
                        ct.scrollBy(ct.getScrollX(), ct.getScrollY() + 500);
                        clickedTextField = true;
                    }
                }
            }
        });
    }



    public void hideKeyboard(View view) {
        ct.scrollTo(ct.getScrollX(), 0);
        InputMethodManager inputMethodManager =(InputMethodManager)getSystemService(MainActivity.INPUT_METHOD_SERVICE);
        inputMethodManager.hideSoftInputFromWindow(view.getWindowToken(), 0);
        clickedTextField = false;
    }

    public void checkLogin(){
        myThread.sendLogin(login.getText().toString(), passwd.getText().toString());
    }

    public void startLoggedActivity(ArrayList<Door> allDoors){
        Intent intent = new Intent(MainActivity.this, LoggedActivityEx.class);
        Log.i("He llegao", "size--> " + allDoors.size());

        Bundle args = new Bundle();
        args.putSerializable("DoorArrayList",(Serializable)allDoors);
        intent.putExtra("BUNDLE",args);
        startActivity(intent);
        finish();
    }

}
