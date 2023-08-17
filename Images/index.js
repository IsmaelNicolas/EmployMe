const express = require("express");
const mongoose = require("mongoose");
const multer = require("multer");
const cloudinary = require("cloudinary").v2;
const fs = require("fs");
const listEndpoints = require("express-list-endpoints");
const cors = require("cors")

const userRouter = express.Router();
const jobRouter = express.Router();

const app = express();
const port = 3000;

app.use(cors())


const cloudinaryCloudName = process.env.CLOUDINARY_CLOUD_NAME || "dktwgz3ax";
const cloudinaryApiKey = process.env.CLOUDINARY_API_KEY || "814627947713372";
const cloudinaryApiSecret =
  process.env.CLOUDINARY_API_SECRET || "F7OFvhg44a68mP-wPe1MNNnuAsM";

cloudinary.config({
  cloud_name: cloudinaryCloudName,
  api_key: cloudinaryApiKey,
  api_secret: cloudinaryApiSecret,
});

// Configuración de Mongoose y conexión a MongoDB
const password = process.env.passworddb || "toor";
const user = process.env.userdb || "incp";
const host = process.env.hostdb || "localhost";
const database = process.env.database || "microservices";

const dbUrl = `mongodb+srv://${user}:${password}@${host}/${database}?retryWrites=true&w=majority`;

console.log(dbUrl);
mongoose
  .connect(dbUrl, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => {
    console.log("Connected to MongoDB");
  })
  .catch((error) => {
    console.error("Error connecting to MongoDB:", error);
  });

// Definir el modelo de imagen en la base de datos
const ImageSchemaUser = new mongoose.Schema({
  user_id: { type: String, required: true }, // Agregamos user_id
  public_id: String,
  url: String,
  description: String,
});

const ImageSchemaJob = new mongoose.Schema({
  job_id: { type: String, required: true }, // Agregamos user_id
  public_id: String,
  url: String,
  description: String,
});

const ImageUser = mongoose.model("User", ImageSchemaUser);
const ImageJob = mongoose.model("Job", ImageSchemaJob);

// Configuración de multer para subir imágenes
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

// Rutas de la API

userRouter.post("/upload", upload.single("image"), async (req, res) => {
  console.log("Uploading job image...")
  try {
    const { user_id, description } = req.body; // Obtener user_id y description del body

    if (!user_id) {
      return res.status(400).json({ message: "user_id is required" });
    }

    // Guardar el archivo temporalmente
    const tempFilePath = `/tmp/${req.file.originalname}`;
    await fs.promises.writeFile(tempFilePath, req.file.buffer);

    // Subir imagen a Cloudinary
    const result = await cloudinary.uploader.upload(tempFilePath, {
      folder: "images",
    });

    // Eliminar el archivo temporal
    await fs.promises.unlink(tempFilePath);

    // Crear registro en la base de datos
    const newImage = new ImageUser({
      user_id: user_id,
      public_id: result.public_id,
      url: result.secure_url,
      description: description,
    });

    await newImage.save();

    res.status(201).json(newImage);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Error uploading image" });
  }
});

userRouter.get("/images", async (req, res) => {
  console.log("Getting user image...")
  try {
    const user_id = req.query.user_id; // Obtener user_id de la query

    const query = user_id ? { user_id: user_id } : {}; // Construir la query según el user_id

    const images = await ImageUser.find(query);
    console.log("Getting ok")
    res.status(200).json(images);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Error fetching images" });
  }
});

userRouter.delete("/images/:id", async (req, res) => {
  try {
    const user_id = req.query.user_id; // Obtener user_id de la query
    const imageId = req.params.id;

    const image = await ImageUser.findOne({ _id: imageId, user_id: user_id });

    if (!image) {
      return res.status(404).json({ message: "Image not found" });
    }

    // Eliminar imagen de Cloudinary
    await cloudinary.uploader.destroy(image.public_id);

    // Eliminar registro de la base de datos
    await image.remove();

    res.status(200).json({ message: "Image deleted successfully" });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Error deleting image" });
  }
});

jobRouter.post("/upload", upload.single("image"), async (req, res) => {
  console.log("Uploading job image...")
  try {
    const { job_id, description } = req.body; // Obtener job_id y description del body

    if (!job_id) {
      return res.status(400).json({ message: "job_id is required" });
    }

    // Guardar el archivo temporalmente
    const tempFilePath = `/tmp/${req.file.originalname}`;
    await fs.promises.writeFile(tempFilePath, req.file.buffer);

    // Subir imagen a Cloudinary
    const result = await cloudinary.uploader.upload(tempFilePath, {
      folder: "images",
    });

    // Eliminar el archivo temporal
    await fs.promises.unlink(tempFilePath);

    // Crear registro en la base de datos
    const newImage = new ImageJob({
      job_id: job_id,
      public_id: result.public_id,
      url: result.secure_url,
      description: description,
    });

    await newImage.save();
    console.log("Image save")
    res.status(201).json(newImage);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Error uploading image" });
  }
});

jobRouter.get("/images", async (req, res) => {
  console.log("Get job image...")
  try {
    const job_id = req.query.job_id; // Obtener job_id de la query

    const query = job_id ? { job_id: job_id } : {}; // Construir la query según el job_id

    const images = await ImageJob.find(query);
    res.status(200).json(images);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Error fetching images" });
  }
});

jobRouter.delete("/images/:id", async (req, res) => {
  console.log("Deleting job image...")
  try {
    const job_id = req.query.job_id; // Obtener job_id de la query
    const imageId = req.params.id;

    const image = await ImageJob.findOne({ _id: imageId, job_id: job_id });

    if (!image) {
      return res.status(404).json({ message: "Image not found" });
    }

    // Eliminar imagen de Cloudinary
    await cloudinary.uploader.destroy(image.public_id);

    // Eliminar registro de la base de datos
    await image.remove();

    res.status(200).json({ message: "Image deleted successfully" });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Error deleting image" });
  }
});

app.use("/api/user", userRouter);
app.use("/api/jobs", jobRouter);


app.route("/about").get(function (req, res) {
  res.status(200).json({ endpoints: listEndpoints(app) });
});


app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
