package com.example.emotionanalysis

import android.os.Bundle
import android.view.ViewGroup
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_sub.*

class SubActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_sub)

        var edit_text_value:String? = intent.getStringExtra("key1")
        var text_view: TextView = TextView(this)
        text_view.setText(
            edit_text_value
        )
        var layout:ViewGroup = findViewById((R.id.activity_print_message))
        layout.addView(text_view)

        subButton.setOnClickListener {
            finish()
        }
    }

}