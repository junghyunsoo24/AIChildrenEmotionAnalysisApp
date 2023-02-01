package com.example.emotionanalysis

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.EditText
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }

    fun printMessage(view: View){
        var edit_text: EditText = findViewById(R.id.inputText)
        var edit_text_value: String? = edit_text.text.toString()
        var intent_for_print: Intent = Intent(this, SubActivity::class.java)
        intent_for_print.putExtra("key1", edit_text_value)
        startActivity(intent_for_print)
    }
}