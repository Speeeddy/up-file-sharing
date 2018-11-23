package com.example.root.upfiletransfer;

import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.Build;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.WindowManager;

import com.github.paolorotolo.appintro.AppIntro;
import com.github.paolorotolo.appintro.AppIntroFragment;


public class IntroActivity extends AppIntro {

    public static SQLiteDatabase mydatabase,mydatabase2,mydatabase3;
    public String user = "lav";
    String pass = "lol";


    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {

            getWindow().setFlags(WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS,
                    WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS);
        }


        mydatabase2 = openOrCreateDatabase("TrustedContactDBB", MODE_PRIVATE, null);
        mydatabase2.execSQL("CREATE TABLE IF NOT EXISTS Trustno(Sno INT, Username VARCHAR, Password VARCHAR);");
        Cursor resultSet1 = mydatabase2.rawQuery("Select * from Trustno", null);
        resultSet1.moveToFirst();
        if (resultSet1.getCount() == 0) {
            mydatabase2.execSQL("INSERT INTO Trustno VALUES ( 1 , '"+user+"' , '"+pass+"' );");
        } else {
            Intent i = new Intent(getApplicationContext() , SplashActivity.class) ;
            startActivity(i) ;
            finish();
        }


        addSlide(AppIntroFragment.newInstance("Welcome To UP", "A server based file sharing application.",
                R.drawable.my_logo1, ContextCompat.getColor(getApplicationContext(),R.color.slide1)));

        addSlide(AppIntroFragment.newInstance("Login or Create User Account", "Free Usage access." ,
                R.drawable.kek, ContextCompat.getColor(getApplicationContext(),R.color.slide2)));

        addSlide(AppIntroFragment.newInstance("Share Files on a Go!", "Choose from a variety of files. Size no constraint.",
                R.drawable.send, ContextCompat.getColor(getApplicationContext(),R.color.slide3)));


        showSkipButton(false);

    }

    @Override
    public void onSkipPressed(Fragment currentFragment) {
        super.onSkipPressed(currentFragment);
        // Do something when users tap on Skip button.
    }

    @Override
    public void onDonePressed(Fragment currentFragment) {
        super.onDonePressed(currentFragment);
        Intent i = new Intent(getApplicationContext(),MainActivity.class);
        startActivity(i);
        finish();
    }

    @Override
    public void onSlideChanged(@Nullable Fragment oldFragment, @Nullable Fragment newFragment) {
        super.onSlideChanged(oldFragment, newFragment);
        // Do something when the slide changes.
    }
}
