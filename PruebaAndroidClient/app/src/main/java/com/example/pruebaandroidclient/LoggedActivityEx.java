package com.example.pruebaandroidclient;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.os.Bundle;

import java.lang.reflect.Array;
import java.util.ArrayList;

public class LoggedActivityEx extends AppCompatActivity {

    RecyclerView doorRecyclerView;
    DoorAdapter doorAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.fragment_logged);

        doorRecyclerView = (RecyclerView) findViewById(R.id.doorRecycler);


        /* Establece que recyclerView tendrá un layout lineal, en concreto vertical*/
        doorRecyclerView.setLayoutManager(new LinearLayoutManager(this, LinearLayoutManager.VERTICAL, false));

        /*  Indica que cada uno de los items va a tener un tamaño fijo*/
        doorRecyclerView.setHasFixedSize(true);

        /* Establece la  decoración por defecto de cada uno de lo items: una línea de división*/
        doorRecyclerView.addItemDecoration(new DividerItemDecoration(doorRecyclerView.getContext(), DividerItemDecoration.VERTICAL));

        /* Instancia un objeto de la clase MovieAdapter */
        doorAdapter = new DoorAdapter(this.getApplicationContext());

        /* Establece el adaptador asociado a recyclerView */
        doorRecyclerView.setAdapter(doorAdapter);

        /* Pone la animación por defecto de recyclerView */
        doorRecyclerView.setItemAnimator(new DefaultItemAnimator());


        loadSearch();
    }

    public void loadSearch(){

        Door d1 = new Door(1, "yeyo", 1, 0);
        Door d2 = new Door(2, "yeyo1", 1, 0);
        Door d3 = new Door(3, "yeyo2", 1, 0);

        ArrayList<Door> getResults = new ArrayList<>();
        getResults.add(d1);
        getResults.add(d2);
        getResults.add(d3);

        doorAdapter.swap(getResults);
        doorAdapter.notifyDataSetChanged();

    }
}
