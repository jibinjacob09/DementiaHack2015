package com.curesoft.memorybox;

import android.content.Context;
import android.util.Log;

import com.loopj.android.http.*;

import org.json.JSONObject;

import java.io.UnsupportedEncodingException;
import java.nio.charset.UnsupportedCharsetException;

import cz.msebera.android.httpclient.entity.StringEntity;

/**
 * Created by Tornike Natsvlishvili on 11/8/15.
 */
public class MemoryBoxRestClient {
    private static final String TAG = "MemoryBoxRestClient";

    private static final String BASE_URL = "http://mdec.club:5000/";

    private static AsyncHttpClient client = new AsyncHttpClient();

    public static void get(String url, RequestParams params, AsyncHttpResponseHandler responseHandler) {
        client.get(getAbsoluteUrl(url), params, responseHandler);
    }

    public static void post(String url, RequestParams params, AsyncHttpResponseHandler responseHandler) {
        client.post(getAbsoluteUrl(url), params, responseHandler);
    }

    public static void post(Context context, String url, JSONObject obj, AsyncHttpResponseHandler responseHandler) {
        StringEntity entity = null;
        try {
            entity = new StringEntity(obj.toString());
        } catch (UnsupportedEncodingException e){
            Log.e(TAG, "Unsupported encoding", e);
        }
        client.post(context, getAbsoluteUrl(url), entity, "application/json", responseHandler);
    }

    private static String getAbsoluteUrl(String relativeUrl) {
        return BASE_URL + relativeUrl;
    }
}
