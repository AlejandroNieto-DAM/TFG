package com.example.pruebaandroidclient;

import androidx.appcompat.app.AppCompatActivity;
import androidx.constraintlayout.widget.ConstraintLayout;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Parcelable;
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

    ConstraintLayout ct;
    Boolean clickedTextField = false;
    public static ClientThread myThread;

    SharedPreferences settings;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        StrictMode.ThreadPolicy policy = new
                StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        MainActivity.myThread = new ClientThread(this, this.getApplicationContext());
        MainActivity.myThread.execute();


        login = findViewById(R.id.editText);
        passwd = findViewById(R.id.editText3);
        btnSend = findViewById(R.id.button);
        ct = findViewById(R.id.yeyo);



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

        settings = getSharedPreferences("Login", 0);
        if(!settings.getString("userLogin", "").isEmpty()){
            login.setText(settings.getString("userLogin", ""));
        }

        btnSend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                checkLogin(login.getText().toString(), passwd.getText().toString());
                settings.edit().putString("userLogin", login.getText().toString()).apply();
            }
        });
    }

    public void hideKeyboard(View view) {
        ct.scrollTo(ct.getScrollX(), 0);
        InputMethodManager inputMethodManager =(InputMethodManager)getSystemService(MainActivity.INPUT_METHOD_SERVICE);
        inputMethodManager.hideSoftInputFromWindow(view.getWindowToken(), 0);
        clickedTextField = false;
    }

    public void checkLogin(String login, String pass){
        MainActivity.myThread.sendLogin(login, pass);
    }

    public void startLoggedActivity(ArrayList<Door> allDoors){
        Intent intent = new Intent(MainActivity.this, LoggedActivityEx.class);
        startActivity(intent);
        finish();
    }

}
