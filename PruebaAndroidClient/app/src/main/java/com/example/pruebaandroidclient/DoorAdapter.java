package com.example.pruebaandroidclient;

import android.annotation.SuppressLint;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.Drawable;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.constraintlayout.widget.ConstraintLayout;
import androidx.recyclerview.widget.RecyclerView;

import com.squareup.picasso.Picasso;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;

public class DoorAdapter extends RecyclerView.Adapter<DoorAdapter.doorViewHolder> {

    public final Context context; //Almacena el contexto donde se ejecutará
    private ArrayList<Door> list; //Almacenará las películas a mostrar
    private DoorAdapter.OnItemClickListener listener; //Listener para cuando se haga click


    //Defino un interface con el OnItemClickListener
    public interface OnItemClickListener {
        void onItemClick(Door movie);
    }

    /*
    Constructor
    */
    public DoorAdapter(Context context) {
        this.list = new ArrayList<Door>();
        this.context = context;
        setListener();
    }

    /*
    Asocio al atributo listener el onItemClickListener correspondiente y sobreescribo el método onItemClick pasando como
    argumento una película
    */
    private void setListener () {
        this.listener = new DoorAdapter.OnItemClickListener() {
            @Override
            public void onItemClick(Door movie) {

            }
        };
    }

    /*
    Sobreescribo onCreateViewHolder, donde  "inflo" la vista de cada item  y devuelve el viewholder que se crea pasándole la vista
    como parámetro
    */
    @Override
    public doorViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {

        View itemView = LayoutInflater.from(parent.getContext()).inflate(R.layout.layout_door_item, parent, false);
        doorViewHolder tvh = new doorViewHolder(itemView);
        return tvh;
    }

    /*
    Sobreescribe onViewHolder, haciendo que muestre la película que hay en el arraylist list en la posición que pasamos como
    parámetro
     */
    @Override
    public void onBindViewHolder(doorViewHolder holder, int position) {

        final Door movie = list.get(position);

        holder.bindMovie(movie, listener);

    }

    /*
    Sobreescribe getItemCount devolviendo el número de películas que tenemos en el arraylist list.
     */
    @Override
    public int getItemCount() {
        return list.size();
    }

    /*
    Defino el viewHolder anidado que hereda de Recycler.ViewHolder necesario para que funcione el adaptador
     */
    public class doorViewHolder extends RecyclerView.ViewHolder {
        /*
        Atributos
         */
        TextView identifier_name;
        ImageView image;
        ConstraintLayout changeColour;

        /*
            Constructor, enlazo los atributos con los elementos del layout
         */
        public doorViewHolder(View itemView) {
            super(itemView);
            identifier_name = (TextView) itemView.findViewById(R.id.textView2);
            image = (ImageView) itemView.findViewById(R.id.imageView);
            changeColour = (ConstraintLayout) itemView.findViewById(R.id.changeColour);


        }

        /*
        Defino un método que servirá para poner los datos de la película en los correspondientes textviews del layout e
        invocará al listener del adaptador cuando se haga click sobre la vista del viewHolder.
         */
        public void bindMovie(final Door movie, final DoorAdapter.OnItemClickListener listener) {
            identifier_name.setText(movie.getIdentifier_name());
            // load image
            try {
                // get input stream
                InputStream ims = context.getAssets().open("logo.png");
                // load image as Drawable
                Drawable d = Drawable.createFromStream(ims, null);
                // set image to ImageView
                image.setImageDrawable(d);
            }
            catch( IOException ex) {
                Log.i("EXCEPTIOM", ex.toString());
                return;
            }

            //Log.i("Aqui en el adaptador", "ye" + movie.getUrlphoto());
            //Picasso.get().load(movie.getUrlphoto()).into(image);

            if(movie.getState() == 1){
                changeColour.setBackground(context.getResources().getDrawable(R.drawable.shape_button_clitemopen));
            } else {
                changeColour.setBackground(context.getResources().getDrawable(R.drawable.shape_button_clitem));
            }

            /*Coloco el Listener a la vista)*/
            itemView.setOnClickListener(new View.OnClickListener() {
                @Override public void onClick(View v) {
                    listener.onItemClick(movie);


                    if(movie.getState() == 1){
                        MainActivity.myThread.sendCloseDoor(movie.getId());
                        movie.setState(0);
                    } else {
                        MainActivity.myThread.sendOpenDoor(movie.getId());
                        movie.setState(1);
                    }



                }
            });
        }
    }

    /*
    Método que limpia el array list de contenidos, carga los nuevos contenidos que se le pasan por parámetro e invoca a
    notifyDataSetChanged para hacer que se refresque la vista del RecyclerView
     */
    public void swap(List<Door> newListMovies) {
        list.clear();
        list.addAll(newListMovies);
        notifyDataSetChanged();
    }


}