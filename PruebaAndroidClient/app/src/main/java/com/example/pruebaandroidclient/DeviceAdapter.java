package com.example.pruebaandroidclient;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.constraintlayout.widget.ConstraintLayout;
import androidx.recyclerview.widget.RecyclerView;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class DeviceAdapter extends RecyclerView.Adapter<DeviceAdapter.doorViewHolder> {

    public final Context context; //Stores the context where it will run
    private ArrayList<Device> list; //Will store the devices to display
    private DeviceAdapter.OnItemClickListener listener; //Listener for when clicked


    //I define an interface with the OnItemClickListener
    public interface OnItemClickListener {
        void onItemClick(Device movie);
    }

    /**
     Constructor
    */
    public DeviceAdapter(Context context) {
        this.list = new ArrayList<Device>();
        this.context = context;
        setListener();
    }

    /**
     I associate the listener attribute with the corresponding onItemClickListener and override the onItemClick method passing as
     argument a devices
    */
    private void setListener () {
        this.listener = new DeviceAdapter.OnItemClickListener() {
            @Override
            public void onItemClick(Device device) {

            }
        };
    }

    /**
    I override onCreateViewHolder, where I "inflate" the view of each item and return the viewholder that is created by passing it the view
    as parameter
    */
    @Override
    public doorViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {

        View itemView = LayoutInflater.from(parent.getContext()).inflate(R.layout.layout_device_item, parent, false);
        doorViewHolder tvh = new doorViewHolder(itemView);
        return tvh;
    }

    /**
    Overwrite onViewHolder, causing it to display the device in the arraylist list at the position we passed as
    parameter
     */
    @Override
    public void onBindViewHolder(doorViewHolder holder, int position) {

        final Device device = list.get(position);
        try {
            holder.bindMovie(device, listener);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
    Override getItemCount by returning the number of devices we have in the arraylist list.
     */
    @Override
    public int getItemCount() {
        return list.size();
    }

    /**
    I define the nested viewHolder inheriting from Recycler.ViewHolder required for the adapter to work
     */
    public class doorViewHolder extends RecyclerView.ViewHolder {
        /**
        Attributes
         */
        TextView identifier_name;
        ImageView image;
        ConstraintLayout changeColour;

        /**
         Constructor, I link the attributes with the elements of the layout
         */
        public doorViewHolder(View itemView) {
            super(itemView);
            identifier_name = (TextView) itemView.findViewById(R.id.deviceIdentifierName);
            image = (ImageView) itemView.findViewById(R.id.cicleImage);
            changeColour = (ConstraintLayout) itemView.findViewById(R.id.ctDevice);


        }

        /**
        I define a method that will be used to put the device data in the corresponding textviews of the layout and
        will invoke the adapter listener when the viewHolder view is clicked
         */
        public void bindMovie(final Device device, final DeviceAdapter.OnItemClickListener listener) throws IOException {
            identifier_name.setText(device.getIdentifier_name());

            byte[] imageBytes = device.getImage();
            Bitmap bm = BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.length);
            image.setImageBitmap(bm);

            if(device.getState() == 1){
                changeColour.setBackground(context.getResources().getDrawable(R.drawable.shape_button_clitemopen));
            } else {
                changeColour.setBackground(context.getResources().getDrawable(R.drawable.shape_button_clitem));
            }

            /** I place the listener in the view of the item*/
            itemView.setOnClickListener(new View.OnClickListener() {
                @Override public void onClick(View v) {
                    listener.onItemClick(device);


                    if(device.getState() == 1){
                        MainActivity.myThread.sendCloseDevice(device.getId());
                        device.setState(0);
                    } else {
                        MainActivity.myThread.sendOpenDevice(device.getId());
                        device.setState(1);
                    }



                }
            });
        }
    }

    /**
    Method that cleans the content of the list array, loads the new contents passed to it by parameter and invokes
    notifyDataSetChanged to refresh the RecyclerView view
     */
    public void swap(List<Device> newListDevice) {
        list.clear();
        list.addAll(newListDevice);
        notifyDataSetChanged();
    }

}
