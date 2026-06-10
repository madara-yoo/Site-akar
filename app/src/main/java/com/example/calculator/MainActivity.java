package com.example.calculator;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {
    private TextView display;
    private String current = "";
    private String operator = "";
    private double first = Double.NaN;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        display = findViewById(R.id.display);
        display.setText("0");

        int[] ids = new int[]{
                R.id.btn0, R.id.btn1, R.id.btn2, R.id.btn3,
                R.id.btn4, R.id.btn5, R.id.btn6, R.id.btn7,
                R.id.btn8, R.id.btn9, R.id.btnDot,
                R.id.btnAdd, R.id.btnSub, R.id.btnMul, R.id.btnDiv,
                R.id.btnEq, R.id.btnClear
        };

        for (int id : ids) {
            View v = findViewById(id);
            if (v != null) v.setOnClickListener(this);
        }
    }

    @Override
    public void onClick(View v) {
        int id = v.getId();
        if (id == R.id.btn0) append("0");
        else if (id == R.id.btn1) append("1");
        else if (id == R.id.btn2) append("2");
        else if (id == R.id.btn3) append("3");
        else if (id == R.id.btn4) append("4");
        else if (id == R.id.btn5) append("5");
        else if (id == R.id.btn6) append("6");
        else if (id == R.id.btn7) append("7");
        else if (id == R.id.btn8) append("8");
        else if (id == R.id.btn9) append("9");
        else if (id == R.id.btnDot) appendDot();
        else if (id == R.id.btnAdd) setOperator("+");
        else if (id == R.id.btnSub) setOperator("-");
        else if (id == R.id.btnMul) setOperator("*");
        else if (id == R.id.btnDiv) setOperator("/");
        else if (id == R.id.btnEq) calculate();
        else if (id == R.id.btnClear) clear();
    }

    private void append(String s) {
        if (current.equals("0")) current = s; else current += s;
        display.setText(current);
    }

    private void appendDot() {
        if (!current.contains(".")) {
            if (current.isEmpty()) current = "0."; else current += ".";
            display.setText(current);
        }
    }

    private void setOperator(String op) {
        if (!Double.isNaN(first) && !current.isEmpty()) {
            calculate();
        }
        try {
            first = current.isEmpty() ? 0 : Double.parseDouble(current);
        } catch (NumberFormatException e) {
            first = 0;
        }
        operator = op;
        current = "";
    }

    private void calculate() {
        if (operator.isEmpty() || Double.isNaN(first)) return;
        double second;
        try {
            second = current.isEmpty() ? 0 : Double.parseDouble(current);
        } catch (NumberFormatException e) {
            second = 0;
        }
        double result = 0;
        switch (operator) {
            case "+": result = first + second; break;
            case "-": result = first - second; break;
            case "*": result = first * second; break;
            case "/":
                if (second == 0) {
                    Toast.makeText(this, "Division by zero", Toast.LENGTH_SHORT).show();
                    clear();
                    return;
                } else {
                    result = first / second;
                }
                break;
        }
        // display result and prepare for further operations
        if (Math.floor(result) == result) display.setText(String.valueOf((long)result));
        else display.setText(String.valueOf(result));
        current = String.valueOf(result);
        first = Double.NaN;
        operator = "";
    }

    private void clear() {
        current = "";
        operator = "";
        first = Double.NaN;
        display.setText("0");
    }
}
