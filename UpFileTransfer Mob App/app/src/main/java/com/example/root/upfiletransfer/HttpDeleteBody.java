package com.example.root.upfiletransfer;

import org.apache.http.client.methods.HttpEntityEnclosingRequestBase;

import java.net.URI;

public class HttpDeleteBody extends HttpEntityEnclosingRequestBase {

    public static final String METHOD_NAME = "DELETE";
    public String getMethod() {
        return METHOD_NAME;
    }

    public HttpDeleteBody(final String uri) {
        super();
        setURI(URI.create(uri));
    }

    public HttpDeleteBody(final URI uri) {
        super();
        setURI(uri);
    }

    public HttpDeleteBody() {
        super();
    }
}
