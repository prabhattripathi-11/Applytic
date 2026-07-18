import multer from "multer";
import path from "path";
import fs from "fs";

/**
 * Ensure uploads directory exists.
 */
const uploadDir = path.join(process.cwd(), "uploads");

if (!fs.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir, { recursive: true });
}

/**
 * Configure where uploaded resumes are stored.
 */
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, uploadDir);
    },

    filename: (req, file, cb) => {
        const uniqueName =
            Date.now() + "-" + file.originalname.replace(/\s+/g, "_");

        cb(null, uniqueName);
    },
});

/**
 * Accept only PDF files.
 */
const fileFilter: multer.Options["fileFilter"] = (req, file, cb) => {

    if (file.mimetype !== "application/pdf") {
        cb(new Error("Only PDF files are allowed."));
        return;
    }

    cb(null, true);
};

/**
 * Export configured Multer middleware.
 */
export const upload = multer({
    storage,
    fileFilter,
    limits: {
        fileSize: 5 * 1024 * 1024, // 5 MB
    },
});