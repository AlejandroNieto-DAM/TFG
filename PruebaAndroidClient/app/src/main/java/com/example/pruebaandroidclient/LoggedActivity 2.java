package com.example.pruebaandroidclient;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import com.example.pruebaandroidclient.RandomPhotoClasses.RetrofitCall.DoorService;
import com.example.pruebaandroidclient.RandomPhotoClasses.RandomImage;
import com.example.pruebaandroidclient.RandomPhotoClasses.RetrofitCall.RetrofitInstance;
import com.squareup.picasso.Picasso;

import java.util.ArrayList;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class LoggedActivity extends AppCompatActivity {

    private RecyclerView doorRecyclerView;
    private DeviceAdapter deviceAdapter;
    private ImageView randomPhoto;
    private Button btnLogout;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.logged_activity);

        MainActivity.myThread.setMyLoggedActivity(this);

        btnLogout = (Button) findViewById(R.id.buttonLogout);

        doorRecyclerView = (RecyclerView) findViewById(R.id.deviceRecyclerView);
        randomPhoto = (ImageView) findViewById(R.id.backgroundImage);

        /* Establish that the recycler view will have a lineal layout, in specefic 'vertical' */
        doorRecyclerView.setLayoutManager(new LinearLayoutManager(this, LinearLayoutManager.VERTICAL, false));

        /*  All the items will have the same size */
        doorRecyclerView.setHasFixedSize(true);

        /* Instance of the object DeviceAdapter */
        deviceAdapter = new DeviceAdapter(this);

        /* Set the previous instance of the adapter to the recycler view */
        doorRecyclerView.setAdapter(deviceAdapter);

        /* Set the default animation in the recycler view */
        doorRecyclerView.setItemAnimator(new DefaultItemAnimator());

        btnLogout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                MainActivity.myThread.setFinished();
                Intent i = getBaseContext().getPackageManager().
                        getLaunchIntentForPackage(getBaseContext().getPackageName());
                i.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
                i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                startActivity(i);
                finish();
            }
        });

        loadImage();
        loadDoors();

    }

    /**
     * @brief Get all the devices of the MainActivity and pass them to the DeviceAdapter to do the RecyclerView.
     * @pre The loggin has to be successful.
     * @post The DeviceAdapter will load al the devices.
     */
    public void loadDoors(){
        ArrayList<Device> allDevices = MainActivity.myThread.getAllDevices();
        deviceAdapter.swap(allDevices);
        deviceAdapter.notifyDataSetChanged();
    }

    /**
     * @brief When one device state has changed this method says to the adapter that some has changed to repaint the RecyclerView.
     * @pre RecyclerView has to load some information previous to call this method.
     * @post RecyclerView will be repainted.
     */
    public void refresh(ArrayList<Device> allDevices){
        runOnUiThread(new Runnable() {
            public void run() {

                deviceAdapter.swap(allDevices);
                deviceAdapter.notifyDataSetChanged();
            }
        });
    }

    /**
     * @brief Call to retrofit to get a random image from one API to load it in the ImageView.
     * @pre Internet permissions on manifest.
     * @post One image random from api will be loaded into the ImageView
     */
    private void loadImage(){
        /* Instance of retrofit */
        DoorService getImage = RetrofitInstance.getRetrofitInstance().create(DoorService.class);
        /* The parameters of the function call are defined getRandomPhoto */
        Call<RandomImage> call = getImage.getRandomPhoto(RetrofitInstance.getApiKey());
        /* Async call to the API */
        call.enqueue(new Callback<RandomImage>() {
            @Override
            public void onResponse(Call<RandomImage> call, Response<RandomImage> response) {
                switch (response.code()) {
                    /* Successful call */
                    case 200:
                        /* In the object data of the class RandomImage is stored the JSON converted to objects */
                        RandomImage data = response.body();
                        try{
                            Picasso.get().load(data.getUrls().getRegular()).into(randomPhoto);
                        } catch(RuntimeException e){

                        }
                        break;
                    case 401:
                        break;
                    default:
                        break;
                }
            }

            @Override
            public void onFailure(Call<RandomImage> call, Throwable t) {
                Toast.makeText(getBaseContext(), "Error loading background photo...", Toast.LENGTH_SHORT).show();
            }
        });



    }
}
