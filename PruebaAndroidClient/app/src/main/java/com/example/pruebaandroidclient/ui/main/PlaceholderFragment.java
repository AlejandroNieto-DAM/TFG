package com.example.pruebaandroidclient.ui.main;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.Nullable;
import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProviders;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.example.pruebaandroidclient.LoggedActivity;
import com.example.pruebaandroidclient.MainActivity;
import com.example.pruebaandroidclient.R;
import com.squareup.picasso.Picasso;

import java.io.File;
import java.util.ArrayList;

/**
 * A placeholder fragment containing a simple view.
 */
public class PlaceholderFragment extends Fragment {

    private static final String ARG_SECTION_NUMBER = "section_number";

    private PageViewModel pageViewModel;
    Button door1;
    Button door2;

    public static PlaceholderFragment newInstance(int index) {
        PlaceholderFragment fragment = new PlaceholderFragment();
        Bundle bundle = new Bundle();
        bundle.putInt(ARG_SECTION_NUMBER, index);
        fragment.setArguments(bundle);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        pageViewModel = ViewModelProviders.of(this).get(PageViewModel.class);
        int index = 1;
        if (getArguments() != null) {
            index = getArguments().getInt(ARG_SECTION_NUMBER);
        }
        pageViewModel.setIndex(index);
    }

    @Override
    public View onCreateView(
            @NonNull LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState) {
        View root = inflater.inflate(R.layout.fragment_logged, container, false);
        final TextView textView = root.findViewById(R.id.section_label);

        door1 = (Button) root.findViewById(R.id.button3);
        door2 = (Button) root.findViewById(R.id.button2);

        //TODO CONSULTAR ESTADO DE LAS PUERTAS Y CAMBIAR COLOR
        try {
            checkDoor1();
            checkDoor2();
        } catch (AuthFailureError authFailureError) {
            authFailureError.printStackTrace();
        }

        door1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //TODO MANDAR PETICION AL SERVIDOR PARA CAMBIAR EL ESTADO DE LAS PUERTAS

            }
        });

        door2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

            }
        });



        pageViewModel.getText().observe(getViewLifecycleOwner(), new Observer<String>() {
            @Override
            public void onChanged(@Nullable String s) {
                textView.setText(s);
            }
        });
        return root;
    }

    private void checkDoor1() throws AuthFailureError {
        RequestQueue queue = Volley.newRequestQueue(getContext());
        String url ="http://192.168.1.135/login/door.php?idDoor=" + 1;

        // Request a string response from the provided URL.
        StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        // Display the first 500 characters of the response string.
                        //textView.setText("Response is: "+ response.substring(0,500));

                        if(!response.toString().equals("[ ]")){

                            String getState = response.substring(response.indexOf("state") + 8, response.length() - 3);
                            boolean state = false;
                            if(getState.equals("1")){
                                door1.setBackgroundColor(Color.GREEN);
                            } else {
                                door1.setBackgroundColor(Color.RED);
                            }

                        }
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                //textView.setText("That didn't work!");
            }
        });
        queue.add(stringRequest);
    }

    private void checkDoor2() throws AuthFailureError {
        RequestQueue queue = Volley.newRequestQueue(getContext());
        String url ="http://192.168.1.135/login/door.php?idDoor=" + 2;

        // Request a string response from the provided URL.
        StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        // Display the first 500 characters of the response string.
                        //textView.setText("Response is: "+ response.substring(0,500));

                        if(!response.toString().equals("[ ]")){

                            String getState = response.substring(response.indexOf("state") + 8, response.length() - 3);
                            boolean state = false;
                            if(getState.equals("1")){
                                door2.setBackgroundColor(Color.GREEN);
                            } else {
                                door2.setBackgroundColor(Color.RED);
                            }

                        }
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                //textView.setText("That didn't work!");
            }
        });
        queue.add(stringRequest);
    }

    private void changeDoorState(int state, int idDoor){

    }
}