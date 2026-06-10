package com.example.calculator;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    private TextView display;
    private double first = Double.NaN;
    private double second;
    private char currentOp;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        display = findViewById(R.id.display);

        int[] digits = {R.id.btn0,R.id.btn1,R.id.btn2,R.id.btn3,R.id.btn4,R.id.btn5,R.id.btn6,R.id.btn7,R.id.btn8,R.id.btn9};
        for (int id: digits) findViewById(id).setOnClickListener(this::onDigit);
        findViewById(R.id.btnDot).setOnClickListener(this::onDot);
        findViewById(R.id.btnPlus).setOnClickListener(this::onOp);
        findViewById(R.id.btnMinus).setOnClickListener(this::onOp);
        findViewById(R.id.btnMul).setOnClickListener(this::onOp);
        findViewById(R.id.btnDiv).setOnClickListener(this::onOp);
        findViewById(R.id.btnEq).setOnClickListener(v -> onEqual());
        findViewById(R.id.btnC).setOnClickListener(v -> { display.setText(""); first = Double.NaN; currentOp = 0; });
    }

    private void onDigit(View v) {
        Button b = (Button)v; display.append(b.getText());
    }
    private void onDot(View v) { if (!display.getText().toString().contains(".")) display.append("."); }
    private void onOp(View v) {
        if (!Double.isNaN(first)) { onEqual(); }
        try { first = Double.parseDouble(display.getText().toString()); } catch(Exception e){ first = 0; }
        Button b = (Button)v; currentOp = b.getText().charAt(0); display.setText("");
    }
    private void onEqual() {
        try { second = Double.parseDouble(display.getText().toString()); } catch(Exception e){ second = 0; }
        double result = 0;
        switch (currentOp) {
            case '+': result = first + second; break;
            case '-': result = first - second; break;
            case '×': case '*': result = first * second; break;
            case '÷': case '/': result = (second==0? Double.NaN : first / second); break;
            default: result = second; break;
        }
        display.setText(String.valueOf(result));
        first = Double.NaN; currentOp = 0;
    }
}
