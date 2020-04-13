package com.example.pruebaandroidclient;

import androidx.appcompat.app.AppCompatActivity;
import androidx.constraintlayout.widget.ConstraintLayout;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.sip.SipAudioCall;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.WindowManager;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.squareup.picasso.Picasso;

import org.json.JSONObject;

import java.io.File;

import javax.xml.transform.ErrorListener;
import javax.xml.transform.TransformerException;

public class MainActivity extends AppCompatActivity{

    TextView login;
    TextView passwd;
    Button btnSend;
    ImageView minimap;

    ConstraintLayout ct;
    Boolean clickedTextField = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        login = findViewById(R.id.editText);
        passwd = findViewById(R.id.editText3);
        btnSend = findViewById(R.id.button);
        minimap = findViewById(R.id.imageView3);
        ct = findViewById(R.id.yeyo);



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
        RequestQueue queue = Volley.newRequestQueue(this);
        String url ="http://192.168.1.135/login/sesion.php?user=" + login.getText().toString() + "&pwd="+ passwd.getText().toString();

        // Request a string response from the provided URL.
        StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        // Display the first 500 characters of the response string.
                        //textView.setText("Response is: "+ response.substring(0,500));

                        if(!response.toString().equals("[]")){
                            Log.i("Miralo" , response.toString());
                            Intent intent = new Intent(MainActivity.this, LoggedActivity.class);
                            intent.putExtra("CompleteName", response.toString().substring(response.toString().indexOf("nombreCompleto") + 17, response.toString().length() - 3));
                            startActivity(intent);
                            finish();
                        }
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                //textView.setText("That didn't work!");
            }
        });

        // Add the request to the RequestQueue.

        queue.add(stringRequest);
    }

}
