package com.example.root.upfiletransfer;

import android.app.NotificationManager;
import android.content.Context;
import android.content.Intent;
import android.database.sqlite.SQLiteDatabase;
import android.os.AsyncTask;
import android.os.Build;
import android.support.design.widget.Snackbar;
import android.support.design.widget.TextInputEditText;
import android.support.design.widget.TextInputLayout;
import android.support.v4.app.NotificationCompat;
import android.support.v4.widget.NestedScrollView;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.AppCompatButton;
import android.support.v7.widget.AppCompatTextView;
import android.support.v7.widget.CardView;
import android.util.Log;
import android.view.KeyEvent;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import org.json.JSONException;
import org.json.JSONObject;
import org.w3c.dom.Text;

import java.io.IOException;
import java.io.UnsupportedEncodingException;

public class LoginActivity extends AppCompatActivity {

    EditText t;
    EditText lUsername , lPassword;
    TextView log;
    CardView logind;
    TextView reg ;
    private Session session;
    public String hue = "" ;
    private final AppCompatActivity activity = LoginActivity.this;
    public static SQLiteDatabase mydatabase,mydatabase2,mydatabase3;

//    private InputValidation inputValidation;
    private DatabaseHelper databaseHelper;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {

            getWindow().setFlags(WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS,
                    WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS);
        }


        session = new Session(this);
        databaseHelper = new DatabaseHelper(this);
//        t = (EditText) findViewById(R.id.username);
        log = (TextView) findViewById(R.id.textView);
        lUsername = (EditText) findViewById(R.id.lUsername) ;
        lPassword = (EditText) findViewById(R.id.lPassword) ;
        reg = (TextView) findViewById(R.id.register);



        logind = (CardView) findViewById(R.id.logindd) ;
        mydatabase = openOrCreateDatabase("TrustedContactDB", MODE_PRIVATE, null);
        mydatabase.execSQL("CREATE TABLE IF NOT EXISTS Trust(Sno INT, Username String, Password VARCHAR);");

        logind.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                JSONObject jsonObject = new JSONObject() ;
                try {
                    jsonObject.put("username" , lUsername.getText().toString()) ;
                    jsonObject.put("password" , lPassword.getText().toString()) ;
                    hue = jsonObject.toString(1) ;

                    new AsyncTask<Void , Void , String>(){

                        @Override
                        protected String doInBackground(Void... voids) {
                            return getServerResponse(hue) ;
                        }

                        @Override
                        protected void onPostExecute(String s) {
                            s = s.replaceAll("\\s+","");
                            if(s.trim().toString().equals("\"Verified\"")){
                                String user = lUsername.getText().toString() ;
                                String pass = lPassword.getText().toString() ;
                                int log = 1;
                                mydatabase.execSQL("DELETE FROM Trust WHERE Sno=1");
                                mydatabase.execSQL("INSERT INTO Trust VALUES ( 1 , '"+user+"' , '"+pass+"' );");
                                Intent i = new Intent(getApplicationContext() , SendReceive.class) ;
                                i.putExtra("username" , lUsername.getText().toString()) ;
                                i.putExtra("logged" , log) ;
                                startActivity(i);
                                finish() ;
                            }else{
                                Toast.makeText(getApplicationContext() , s , Toast.LENGTH_LONG).show();
                            }
                        }
                    }.execute() ;
                } catch (JSONException e) {
                    e.printStackTrace();
                }


            }
        });


//        if(session.loggedIn()){
//            startActivity(new Intent(LoginActivity.this , MainActivity.class));
//            finish();
//        }

//        log.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View v) {
//                JSONObject jsonObject = new JSONObject() ;
//                try {
//                    jsonObject.put("username" , lUsername.getText().toString()) ;
//                    jsonObject.put("password" , lPassword.getText().toString()) ;
//                    hue = jsonObject.toString(1) ;
//
//                    new AsyncTask<Void , Void , String>(){
//
//                        @Override
//                        protected String doInBackground(Void... voids) {
//                            return getServerResponse(hue) ;
//                        }
//
//                        @Override
//                        protected void onPostExecute(String s) {
//                            s = s.replaceAll("\\s+","");
//                            if(s.trim().toString().equals("\"Verified\"")){
//                                String user = lUsername.getText().toString() ;
//                                String pass = lPassword.getText().toString() ;
//                                int log = 1;
//                                mydatabase.execSQL("DELETE FROM Trust WHERE Sno=1");
//                                mydatabase.execSQL("INSERT INTO Trust VALUES ( 1 , '"+user+"' , '"+pass+"' );");
//                                Intent i = new Intent(getApplicationContext() , SendReceive.class) ;
//                                i.putExtra("username" , lUsername.getText().toString()) ;
//                                i.putExtra("logged" , log) ;
//                                startActivity(i);
//                                finish() ;
//                            }else{
//                                Toast.makeText(getApplicationContext() , "."+s.trim().toString()+"." , Toast.LENGTH_LONG).show();
//                            }
//                        }
//                    }.execute() ;
//                } catch (JSONException e) {
//                    e.printStackTrace();
//                }
//
//            }
//        });

        reg.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(getApplicationContext() , RegisterActivity.class) ;
                startActivity(i) ;
                finish() ;
            }
        });
    }



//    private void login(){
//        String username = t.getText().toString();
////        String pass = etPass.getText().toString();
//
//        if(databaseHelper.getUser(username)){
//            session.setLoggedIn(true);
//            Intent i = new Intent(getApplicationContext() , SendReceive.class);
//            i.putExtra("username" , username);
//            startActivity(i);
//            finish();
//        }else{
//            Toast.makeText(getApplicationContext(), "Wrong email/password",Toast.LENGTH_SHORT).show();
//        }
//    }

//    private void verifyFromSQLite() {
////        if (!inputValidation.isInputEditTextFilled(textInputEditTextEmail, textInputLayoutEmail, getString(R.string.error_message_email))) {
////            return;
////        }
////        if (!inputValidation.isInputEditTextEmail(textInputEditTextEmail, textInputLayoutEmail, getString(R.string.error_message_email))) {
////            return;
////        }
////        if (!inputValidation.isInputEditTextFilled(textInputEditTextPassword, textInputLayoutPassword, getString(R.string.error_message_email))) {
////            return;
////        }
//
//        if (databaseHelper.checkUser(t.getText().toString().trim())){
//
//
//            Intent accountsIntent = new Intent(activity, SendReceive.class);
////            accountsIntent.putExtra("EMAIL", textInputEditTextEmail.getText().toString().trim());
//            emptyInputEditText();
//            startActivity(accountsIntent);
//
//
//        } else {
//            // Snack Bar to show success message that record is wrong
////            Snackbar.make(nestedScrollView, getString(R.string.error_valid_email_password), Snackbar.LENGTH_LONG).show();
//            Toast.makeText(getApplicationContext(),"Invalid Username",Toast.LENGTH_LONG);
//        }
//    }

    private String getServerResponse(String json){
        HttpPost post  = new HttpPost("https://up-karoon.ga/api/um/login");
        String ret = "UNABLE TO CONTACT SERVER" ;
        HttpResponse httpResponse ;
        try {
            StringEntity entity = new StringEntity(json);
            post.setEntity(entity);
            Log.d("Entity" , entity.toString()) ;
            post.setHeader("Content-type" , "application/json");
            DefaultHttpClient client = new DefaultHttpClient();
            httpResponse = client.execute(post) ;
//            ret = client.execute(post , handler);
            ret = EntityUtils.toString(httpResponse.getEntity()) ;
            return ret ;
        } catch (UnsupportedEncodingException e) {
            Log.d("JWP" , e.toString());
        } catch (ClientProtocolException e) {
            Log.d("JWP" , e.toString());
        } catch (IOException e) {
            Log.d("JWP" , e.toString());
        }
        return ret;
    }
    /**
     * This method is to empty all input edit text
     */
    private void emptyInputEditText() {
        t.setText(null);
//        textInputEditTextPassword.setText(null);
    }

    @Override
    public void onBackPressed() {
        moveTaskToBack(true);
        finish();
    }
}
