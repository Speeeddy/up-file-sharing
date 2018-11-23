package com.example.root.upfiletransfer;

import android.Manifest;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.Environment;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import android.graphics.Color;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashMap;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {


//    OkHttpClient client = new OkHttpClient();
    private int STORAGE_PERMISSION_CODE = 1;

    private OkHttpClient okHttpClient;
    private Request request;
    private Session session;
    public String user = "lav";
    String pass = "lol";
    public static SQLiteDatabase mydatabase,mydatabase2,mydatabase3;
    public String url= "http://13.233.85.191:5000/fp/lav";
    Button b,b2;
    EditText t;
    public static final String PREFS_NAME = "LoginPrefs";
    public String st;
    EditText username;
    Button login;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        File file = new File(Environment.getExternalStorageDirectory() + "/UpFileTransfer");

        if(!file.exists()){
            file.mkdirs();
        }

//        if (ContextCompat.checkSelfPermission(MainActivity.this,
//                Manifest.permission.READ_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED) {
//
////            Toast.makeText(SendReceive.this, "You have already granted this permission!",
////                    Toast.LENGTH_SHORT).show();
//        } else {
//            requestStoragePermission();
//        }



//        mydatabase2 = openOrCreateDatabase("TrustedContactDBB", MODE_PRIVATE, null);
//        mydatabase2.execSQL("CREATE TABLE IF NOT EXISTS Trustno(Sno INT, Username VARCHAR, Password VARCHAR);");
//        Cursor resultSet1 = mydatabase2.rawQuery("Select * from Trustno", null);
//        resultSet1.moveToFirst();
//        if (resultSet1.getCount() > 0) {
//
//        } else {
//            mydatabase2.execSQL("INSERT INTO Trustno VALUES ( 1 , '"+user+"' , '"+pass+"' );");
//            Intent i = new Intent(getApplicationContext() , IntroActivity.class) ;
//            startActivity(i) ;
//        }




        mydatabase = openOrCreateDatabase("TrustedContactDB", MODE_PRIVATE, null);
        mydatabase.execSQL("CREATE TABLE IF NOT EXISTS Trust(Sno INT, Username VARCHAR, Password VARCHAR);");
        Cursor resultSet = mydatabase.rawQuery("Select * from Trust", null);
        resultSet.moveToFirst();
        if(resultSet.getCount() > 0){
            String username = resultSet.getString(1) ;
            Intent i = new Intent(getApplicationContext() , SendReceive.class) ;
            i.putExtra("username" , username) ;
            i.putExtra("logged" , 1) ;
            startActivity(i) ;
        }else{
            Intent i = new Intent(getApplicationContext() , LoginActivity.class) ;
            startActivity(i);
            finish() ;
        }
    }


//    private void requestStoragePermission() {
//        if (ActivityCompat.shouldShowRequestPermissionRationale(this,
//                Manifest.permission.READ_EXTERNAL_STORAGE)) {
//
//            new AlertDialog.Builder(this)
//                    .setTitle("Permission needed")
//                    .setMessage("This permission is needed to access files")
//                    .setPositiveButton("ok", new DialogInterface.OnClickListener() {
//                        @Override
//                        public void onClick(DialogInterface dialog, int which) {
//                            ActivityCompat.requestPermissions(MainActivity.this,
//                                    new String[] {Manifest.permission.READ_EXTERNAL_STORAGE}, STORAGE_PERMISSION_CODE);
//                        }
//                    })
//                    .setNegativeButton("cancel", new DialogInterface.OnClickListener() {
//                        @Override
//                        public void onClick(DialogInterface dialog, int which) {
//                            dialog.dismiss();
//                        }
//                    })
//                    .create().show();
//
//        } else {
//            ActivityCompat.requestPermissions(this,
//                    new String[] {Manifest.permission.READ_EXTERNAL_STORAGE}, STORAGE_PERMISSION_CODE);
//        }
//    }
//
//    @Override
//    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
//        if (requestCode == STORAGE_PERMISSION_CODE)  {
//            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
//                Toast.makeText(this, "Permission GRANTED", Toast.LENGTH_SHORT).show();
//            } else {
//                Toast.makeText(this, "Permission DENIED", Toast.LENGTH_SHORT).show();
//                Intent i = new Intent(getApplicationContext() , IntroActivity.class);
//                startActivity(i);
//                finish();
//            }
//        }
//    }

    private void logout() {
        session.setLogin(false);
        finish();
        startActivity(new Intent(MainActivity.this , LoginActivity.class));
    }
}
