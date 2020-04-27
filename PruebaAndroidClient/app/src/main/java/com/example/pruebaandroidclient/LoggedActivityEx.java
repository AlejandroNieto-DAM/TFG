package com.example.pruebaandroidclient;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
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

public class LoggedActivityEx extends AppCompatActivity {

    RecyclerView doorRecyclerView;
    DoorAdapter doorAdapter;
    ImageView randomPhoto;
    String photourl = "";
    ArrayList<Door> allDoors;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.fragment_logged);


        Intent intent = getIntent();
        Bundle args = intent.getBundleExtra("BUNDLE");
        allDoors = (ArrayList<Door>) args.getSerializable("DoorArrayList");
        MainActivity.myThread.setMyLoggedActivity(this);


        doorRecyclerView = (RecyclerView) findViewById(R.id.doorRecycler);
        randomPhoto = (ImageView) findViewById(R.id.imageView2);

        /* Establece que recyclerView tendrá un layout lineal, en concreto vertical*/
        doorRecyclerView.setLayoutManager(new LinearLayoutManager(this, LinearLayoutManager.VERTICAL, false));

        /*  Indica que cada uno de los items va a tener un tamaño fijo*/
        doorRecyclerView.setHasFixedSize(true);

        /* Establece la  decoración por defecto de cada uno de lo items: una línea de división*/
        //doorRecyclerView.addItemDecoration(new DividerItemDecoration(doorRecyclerView.getContext(), DividerItemDecoration.VERTICAL));

        /* Instancia un objeto de la clase MovieAdapter */
        doorAdapter = new DoorAdapter(this.getApplicationContext());

        /* Establece el adaptador asociado a recyclerView */
        doorRecyclerView.setAdapter(doorAdapter);

        /* Pone la animación por defecto de recyclerView */
        doorRecyclerView.setItemAnimator(new DefaultItemAnimator());

        loadImage();


    }

    public void loadSearch(String url){

        Log.i("eeee", "t" + photourl);
        for(Door d : allDoors){
            d.setUrlphoto(url);
            d.printDoor();
        }


        ArrayList<Door> getResults = new ArrayList<>();
        for(Door d: allDoors){
            getResults.add(d);
        }

        doorAdapter.swap(getResults);
        doorAdapter.notifyDataSetChanged();

    }

    public void loadImage(){
        /* Crea la instanncia de retrofit */
        DoorService getMovie = RetrofitInstance.getRetrofitInstance().create(DoorService.class);
        /* Se definen los parámetros de la llamada a la función getTopRated */
        Call<RandomImage> call = getMovie.getRandomPhoto(RetrofitInstance.getApiKey());
        /* Se hace una llamada asíncrona a la API */
        call.enqueue(new Callback<RandomImage>() {
            @Override
            public void onResponse(Call<RandomImage> call, Response<RandomImage> response) {
                switch (response.code()) {
                    /* En caso de respuesta correcta */
                    case 200:
                        /* En el objeto data de la clase MovieFeed se almacena el JSON convertido a objetos*/
                        RandomImage data = response.body();
                        try{
                            loadSearch(data.getUrls().getRegular());
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
