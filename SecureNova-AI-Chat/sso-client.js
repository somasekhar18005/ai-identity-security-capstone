require("dotenv").config();

const express = require("express");
const { auth } = require("express-openid-connect");

const app = express();

const config = {
  authRequired: false,
  auth0Logout: true,

  secret: process.env.SSO_SESSION_SECRET,
  baseURL: "http://localhost:4000",

  clientID: process.env.SSO_CLIENT_ID,
  clientSecret: process.env.SSO_CLIENT_SECRET,

  issuerBaseURL: process.env.ISSUER_BASE_URL,

  authorizationParams: {
    response_type: "code",
    scope: "openid profile email"
  }
};

app.use(auth(config));

app.get("/", (req, res) => {
  if (req.oidc.isAuthenticated()) {
    res.send(`
      <h1>SecureNova SSO Client</h1>
      <p>Authenticated through Auth0 SSO ✅</p>
      <p>Welcome: ${req.oidc.user.name || req.oidc.user.email}</p>
      <a href="/logout">Logout</a>
    `);
  } else {
    res.send(`
      <h1>SecureNova SSO Client</h1>
      <p>Not authenticated</p>
      <a href="/login">Login with Auth0</a>
    `);
  }
});

app.listen(4000, () => {
  console.log("SSO Client running at http://localhost:4000");
});