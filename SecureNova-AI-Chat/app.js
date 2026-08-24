require("dotenv").config();

const express = require("express");
const { auth: oidcAuth } = require("express-openid-connect");
const {
  auth: jwtAuth,
  requiredScopes
} = require("express-oauth2-jwt-bearer");

const app = express();


// =====================================================
// Auth0 Regular Web Application Configuration
// =====================================================

const config = {
  authRequired: false,
  auth0Logout: true,

  secret: process.env.SESSION_SECRET,
  baseURL: process.env.BASE_URL,

  clientID: process.env.CLIENT_ID,
  clientSecret: process.env.CLIENT_SECRET,

  issuerBaseURL: process.env.ISSUER_BASE_URL,

  authorizationParams: {
    response_type: "code",
    scope: "openid profile email read:ai-data",
    audience: "https://securenova-api",
    prompt: "login"
  }
};


// =====================================================
// Auth0 Login
// =====================================================

app.use(oidcAuth(config));


// =====================================================
// Home
// =====================================================

app.get("/", (req, res) => {

  if (req.oidc.isAuthenticated()) {

    res.send(`
      <h1>SecureNova AI Chat</h1>

      <p>Authenticated successfully with Auth0.</p>

      <p><a href="/profile">View Profile</a></p>

      <p><a href="/token">View Access Token</a></p>

      <p><a href="/api/ai-data">Test Protected API</a></p>

      <p><a href="/logout">Logout</a></p>
    `);

  } else {

    res.send(`
      <h1>SecureNova AI Chat</h1>

      <p>Auth0 authentication test</p>

      <a href="/login">Login with Auth0</a>
    `);
  }
});


// =====================================================
// Profile
// =====================================================

app.get("/profile", (req, res) => {

  if (!req.oidc.isAuthenticated()) {
    return res.status(401).send("Not authenticated");
  }

  res.json(req.oidc.user);
});


// =====================================================
// Access Token - LOCAL LAB ONLY
// =====================================================

app.get("/token", (req, res) => {

  if (!req.oidc.isAuthenticated()) {
    return res.status(401).send("Not authenticated");
  }

  const {
    token_type,
    access_token,
    expires_in
  } = req.oidc.accessToken;

  res.json({
    token_type,
    access_token,
    expires_in
  });
});


// =====================================================
// JWT Protection for SecureNova API
// =====================================================

const checkJwt = jwtAuth({
  issuerBaseURL: `https://${process.env.AUTH0_DOMAIN}`,
  audience: process.env.AUTH0_AUDIENCE
});


// =====================================================
// Protected AI Data Endpoint
// =====================================================

app.get(
  "/api/ai-data",
  checkJwt,
  requiredScopes("read:ai-data"),
  (req, res) => {

    res.status(200).json({
      message: "SecureNova AI data accessed successfully",
      agent: "secure-nova-agent"
    });

  }
);


// =====================================================
// Start Server
// =====================================================

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(
    `SecureNova AI Chat running at http://localhost:${PORT}`
  );
});