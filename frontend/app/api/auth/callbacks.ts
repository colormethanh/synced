// import type { NextApiRequest, NextApiResponse } from 'next';

// export default async function handler(req: NextApiRequest, res: NextApiResponse){
//   const code = req.query.code as string;

//   if (!code) return res.status(400).send("Missing code");

//   try {
//     const response = await fetch("http://localhost:8000/auth/token", {
//       method: "POST"
//     });
//     const data = await response.json();
//     res.status(200).json(data);
//   } catch (err) {
//     res.status(500).json({error: err.message});
//   }
// }
