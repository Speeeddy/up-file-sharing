package com.example.root.upfiletransfer;

import android.content.Context;
import android.content.SharedPreferences;

import android.content.Context;
import android.content.SharedPreferences;
import android.content.SharedPreferences.Editor;
import android.util.Log;
public class Session {
    // Shared preferences file name
    private static final String PREF_NAME = "PrefName";
    private static final String KEY_IS_LOGGEDIN = "isLoggedIn";
    private static final String NAME = "name";
    private static final String EMAIL = "email";
    private static final String FLAG = "flag";
    // LogCat tag
    private static String TAG = Session.class.getSimpleName();
    // Shared Preferences
    SharedPreferences pref;
    Editor editor;
    Context _context;
    // Shared pref mode
    int PRIVATE_MODE = 0;

    public Session(Context context) {
        this._context = context;
        pref = _context.getSharedPreferences(PREF_NAME, PRIVATE_MODE);
        editor = pref.edit();
    }

    public void setLogin(boolean isLoggedIn) {

        editor.putBoolean(KEY_IS_LOGGEDIN, isLoggedIn);

        // commit changes
        editor.commit();

        Log.d(TAG, "User login session modified!");
    }

    public void setUserFlag(String flag) {
        editor.putString(FLAG, flag);
        editor.commit();
    }

    public String getUserEmail() {
        return pref.getString(EMAIL, null);
    }

    public void setUserEmail(String email) {
        editor.putString(EMAIL, email);
        editor.commit();
    }

    public String getFLAG() {
        return pref.getString(FLAG, null);
    }

    public String getUserName() {
        return pref.getString(NAME, null);
    }

    public void setUserName(String name) {
        editor.putString(NAME, name);
        editor.commit();
    }

    public boolean isLoggedIn() {
        return pref.getBoolean(KEY_IS_LOGGEDIN, false);
    }
}