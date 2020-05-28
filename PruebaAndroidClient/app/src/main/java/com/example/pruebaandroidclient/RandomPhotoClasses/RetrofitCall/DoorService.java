package com.example.pruebaandroidclient.RandomPhotoClasses.RetrofitCall;

import com.example.pruebaandroidclient.RandomPhotoClasses.RandomImage;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Query;

public interface DoorService {

    @GET("/photos/random")
    Call<RandomImage> getRandomPhoto(@Query("client_id") String apiKey);

}
