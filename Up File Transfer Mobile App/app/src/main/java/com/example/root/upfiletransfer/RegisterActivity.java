package com.example.root.upfiletransfer;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Build;
import android.support.design.widget.Snackbar;
import android.support.design.widget.TextInputEditText;
import android.support.design.widget.TextInputLayout;
import android.support.v4.widget.NestedScrollView;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.AppCompatButton;
import android.support.v7.widget.AppCompatTextView;
import android.support.v7.widget.CardView;
import android.util.Log;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class RegisterActivity extends AppCompatActivity {


    private final AppCompatActivity activity = RegisterActivity.this;

    private NestedScrollView nestedScrollView;

    private TextInputLayout textInputLayoutName;
    private TextInputLayout textInputLayoutEmail;
    private TextInputLayout textInputLayoutPassword;
    private TextInputLayout textInputLayoutConfirmPassword;

    private TextInputEditText textInputEditTextName;
    private TextInputEditText textInputEditTextEmail;
    private TextInputEditText textInputEditTextPassword;
    private TextInputEditText textInputEditTextConfirmPassword;

    private AppCompatButton appCompatButtonRegister;
    private AppCompatTextView appCompatTextViewLoginLink;

    public String hue = "" ;



//    private InputValidation inputValidation;
    private DatabaseHelper databaseHelper;
    private User user;
    Button b,b2;
    TextView rRegister ;
    EditText rUsername , rEmail , rPassword , rNumber , rName;
    TextView rLogin ;
    CardView card;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {

            getWindow().setFlags(WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS,
                    WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS);
        }


        card = (CardView) findViewById(R.id.card) ;
        rUsername = (EditText) findViewById(R.id.rUsername) ;
        rEmail = (EditText) findViewById(R.id.rEmail) ;
        rPassword = (EditText) findViewById(R.id.rPassword) ;
        rNumber = (EditText) findViewById(R.id.rNumber) ;
        rName = (EditText) findViewById(R.id.rName) ;
        rLogin = (TextView) findViewById(R.id.rLogin) ;
        rRegister = (TextView) findViewById(R.id.rRegister) ;


        card.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(rUsername.getText().toString().trim().equals("") || rEmail.getText().toString().trim().equals("")
                        || rNumber.getText().toString().trim().equals("") || rPassword.getText().toString().trim().equals("")
                        || rName.getText().toString().trim().equals("")){
                    Toast.makeText(getApplicationContext() , "Invalid Credentials" , Toast.LENGTH_LONG).show();
                }else if(!isValidEmail(rEmail.getText().toString())){
                    Toast.makeText(getApplicationContext() , "Invalid Email Address" , Toast.LENGTH_LONG).show();
                }else if(rNumber.getText().toString().length() < 10){
                    Toast.makeText(getApplicationContext() , "Invalid Phone Number" , Toast.LENGTH_LONG).show();
                }else{
                    JSONObject jsonObject = new JSONObject() ;
                    try {
                        jsonObject.put("username" , rUsername.getText().toString()) ;
                        jsonObject.put("email" , rEmail.getText().toString()) ;
                        jsonObject.put("number" , rNumber.getText().toString()) ;
                        jsonObject.put("password" , rPassword.getText().toString()) ;
                        jsonObject.put("name" , rName.getText().toString()) ;
                        hue = jsonObject.toString(1) ;
                        new AsyncTask<Void , Void , String>(){

                            @Override
                            protected String doInBackground(Void... voids) {
                                return getServerResponse(hue);
                            }

                            @Override
                            protected void onPostExecute(String s) {
                                Toast.makeText(getApplicationContext() , s , Toast.LENGTH_LONG).show();
                                Intent i = new Intent(getApplicationContext() , LoginActivity.class) ;
                                startActivity(i) ;
                                finish() ;
                            }
                        }.execute();
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }

            }
        });
        rLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(getApplicationContext() , LoginActivity.class) ;
                startActivity(i);
                finish();
            }
        });

//        rRegister.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View v) {
//                JSONObject jsonObject = new JSONObject() ;
//                try {
//                    jsonObject.put("username" , rUsername.getText().toString()) ;
//                    jsonObject.put("email" , rEmail.getText().toString()) ;
//                    jsonObject.put("number" , rNumber.getText().toString()) ;
//                    jsonObject.put("password" , rPassword.getText().toString()) ;
//                    jsonObject.put("name" , rName.getText().toString()) ;
//                    hue = jsonObject.toString(1) ;
//                    new AsyncTask<Void , Void , String>(){
//
//                        @Override
//                        protected String doInBackground(Void... voids) {
//                            return getServerResponse(hue);
//                        }
//
//                        @Override
//                        protected void onPostExecute(String s) {
//                            Toast.makeText(getApplicationContext() , s , Toast.LENGTH_LONG).show();
//                            Intent i = new Intent(getApplicationContext() , LoginActivity.class) ;
//                            startActivity(i) ;
//                            finish() ;
//                        }
//                    }.execute();
//                } catch (JSONException e) {
//                    e.printStackTrace();
//                }
//
//            }
//        });

        databaseHelper = new DatabaseHelper(this);
        user = new User();

    }



//    private void postDataToSQLite() {
//
//        if (!databaseHelper.checkUser(t.getText().toString().trim())) {
//
//            user.setName(t.getText().toString().trim());
////            user.setEmail(textInputEditTextEmail.getText().toString().trim());
////            user.setPassword(textInputEditTextPassword.getText().toString().trim());
//
//            databaseHelper.addUser(user);
//
//            // Snack Bar to show success message that record saved successfully
////            Snackbar.make(nestedScrollView, getString(R.string.success_message), Snackbar.LENGTH_LONG).show();
//            Toast.makeText(getApplicationContext(),"Success" , Toast.LENGTH_LONG);
//            emptyInputEditText();
//
//
//        } else {
//            // Snack Bar to show error message that record already exists
//            Toast.makeText(getApplicationContext(),"Username Exists" , Toast.LENGTH_LONG);
//        }
//
//
//    }

//    private void emptyInputEditText() {
//        t.setText(null);
////        textInputEditTextEmail.setText(null);
////        textInputEditTextPassword.setText(null);
////        textInputEditTextConfirmPassword.setText(null);
//    }
    public final static boolean isValidEmail(CharSequence target) {
        if (target == null) {
            return false;
        } else {
            return android.util.Patterns.EMAIL_ADDRESS.matcher(target).matches();
        }
    }
    public static boolean isValidEmailAddress(String emailAddress) {
        String emailRegEx;
        Pattern pattern;
        // Regex for a valid email address
        emailRegEx = "^[A-Za-z0-9._%+\\-]+@[A-Za-z0-9.\\-]+\\.[A-Za-z]{2,4}$";
        // Compare the regex with the email address
        pattern = Pattern.compile(emailRegEx);
        Matcher matcher = pattern.matcher(emailAddress);
        if (!matcher.find()) {
            return false;
        }
        return true;
    }
    private String getServerResponse(String json){
        HttpPost post  = new HttpPost("https://up-karoon.ga/api/um/register");
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

    private void displayToast(String message){
        Toast.makeText(getApplicationContext(), message, Toast.LENGTH_SHORT).show();
    }
}
