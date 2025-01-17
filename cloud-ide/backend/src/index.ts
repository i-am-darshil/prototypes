import express, { Request, Response } from 'express';
import cors from 'cors';

const app = express();
const PORT = 4000;

app.use(cors());
app.use(express.json());

// Example API route
app.get('/api/hello', (req: Request, res: Response) => {
    res.json({ message: 'Hello from TypeScript Express!' });
});

app.listen(PORT, () => {
    console.log(`Backend server running at http://localhost:${PORT}`);
});
