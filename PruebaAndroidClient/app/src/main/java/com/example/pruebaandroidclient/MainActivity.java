package com.example.pruebaandroidclient;

import androidx.appcompat.app.AppCompatActivity;
import androidx.constraintlayout.widget.ConstraintLayout;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity{

    private TextView login;
    private TextView passwd;
    private Button btnSend;

    private ConstraintLayout ct;
    private Boolean clickedTextField = false;
    public static ClientThread myThread;

    private SharedPreferences settings;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        StrictMode.ThreadPolicy policy = new
                StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        MainActivity.myThread = new ClientThread(this);
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

    /**
     * @brief Hide the keyboard.
     * @param view which is the view in which we will operate.
     * @pre One of the TextView in the ConstraintLayout has to been touched.
     * @post The view height will be increased.
     **/
    private void hideKeyboard(View view) {
        ct.scrollTo(ct.getScrollX(), 0);
        InputMethodManager inputMethodManager =(InputMethodManager)getSystemService(MainActivity.INPUT_METHOD_SERVICE);
        inputMethodManager.hideSoftInputFromWindow(view.getWindowToken(), 0);
        clickedTextField = false;
    }

    /**
     * @brief Send the first message of protocol by socket to go to the next activity.
     * @param login which is the textview with the login of the person who wants to get logged
     * @param pass which is the textview with the password of the person who wants to get logged
     * @pre One of the TextView in the ConstraintLayout has to been touched.
     * @post The view height will be increased.
     **/
    public void checkLogin(String login, String pass){
        MainActivity.myThread.sendLogin(login, pass);
    }

    /**
     * @brief Starts the activity if the login was successful.
     * @param allDevices which is the textview with the login of the person who wants to get logged.
     * @pre The login has to be succesful and receive all the devices.
     * @post LoggedActivity will be started.
     **/
    public void startLoggedActivity(ArrayList<Device> allDevices){
        Intent intent = new Intent(MainActivity.this, LoggedActivity.class);
        startActivity(intent);
        finish();
    }

    /**
     * @brief this method is called when an error occurs.
     * @pre an error has been occurred
     * @post a toast will show a msg of error
     */
    public void loadToastMsg(){
        runOnUiThread(() -> {
            final Toast toast = Toast.makeText(getApplicationContext(), "Ups...Ha ocurrido un error!", Toast.LENGTH_SHORT);
            toast.show();
        });
    }

}
