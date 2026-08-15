import "dotenv/config";
import express from "express";
import cors from "cors";
import dotenv from "dotenv";

dotenv.config();

const app = express();
const PORT = process.env.BACKEND_PORT || 4000;

app.use(cors());
app.use(express.json());

app.get("/", (_req, res) => {
  res.json({
    message: "AgentHub Backend Running",
    status: "ok",
  });
});

app.listen(PORT, () => {
  console.log(`AgentHub backend running on http://localhost:${PORT}`);
});