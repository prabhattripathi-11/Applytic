import { Request, Response } from "express";
import { parseResume } from "../services/resumeService";

/**
 * Controller responsible for handling resume uploads
 * and forwarding them to the MS2 Resume Matching Service.
 */
export async function uploadAndParseResume(
    req: Request,
    res: Response
): Promise<void> {

    try {

        const file = req.file;

        const { job_description } = req.body;

        if (!file) {
            res.status(400).json({
                success: false,
                message: "Resume PDF is required."
            });
            return;
        }

        if (!job_description) {
            res.status(400).json({
                success: false,
                message: "job_description is required."
            });
            return;
        }

        const result = await parseResume(
            file.path,
            job_description
        );

        res.status(200).json({
            success: true,
            data: result
        });

    } catch (error) {

        console.error("Resume Upload Error:", error);

        res.status(500).json({
            success: false,
            message:
                error instanceof Error
                    ? error.message
                    : "Internal Server Error"
        });
    }
}