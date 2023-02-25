package com.example.ch18_network

//import com.example.ch18_network.retrofit.NetworkService
import android.app.Application

class MyApplication: Application() {

    companion object {
        val QUERY = "travel"

        //val API_KEY = "079dac74a5f94ebdb990ecf61c8854b7"
        //val BASE_URL = "https://newsapi.org"

        val API_KEY = "079dac74a5f94ebdb990ecf61c8854b7"
        val BASE_URL = "https://www.google.co.kr"
        val USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"

    }

}