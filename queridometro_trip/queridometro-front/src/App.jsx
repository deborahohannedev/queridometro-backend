import { useEffect, useState } from "react";
import api from "./api";

function App() {
  const [participants, setParticipants] = useState([]);
  const [emojis, setEmojis] = useState([]);
  const [ranking, setRanking] = useState([]);

  const [voter, setVoter] = useState("");
  const [target, setTarget] = useState("");
  const [emoji, setEmoji] = useState("");
  const [day, setDay] = useState(1);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    const p = await api.get("/participants");
    const e = await api.get("/emojis");
    const r = await api.get("/ranking");

    setParticipants(p.data);
    setEmojis(e.data);
    setRanking(r.data);
  };

  const handleVote = async () => {
    if (!voter || !target || !emoji) {
      alert("Preencha tudo 😅");
      return;
    }

    await api.post("/vote", {
      voter_id: parseInt(voter),
      target_id: parseInt(target),
      emoji_id: parseInt(emoji),
      day_number: parseInt(day),
    });

    alert("Voto enviado 🚀");
    setTarget("");
    setEmoji("");
    fetchData();
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-500 to-indigo-600 flex justify-center p-4">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-xl p-6">

        <h1 className="text-2xl font-bold text-center mb-6">
          🌍 Queridômetro Trip
        </h1>

        {/* VOTAÇÃO */}
        <div className="space-y-4">

          <select
            className="w-full p-3 rounded-xl border"
            onChange={(e) => setVoter(e.target.value)}
          >
            <option value="">Você é...</option>
            {participants.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name}
              </option>
            ))}
          </select>

          <select
            className="w-full p-3 rounded-xl border"
            onChange={(e) => setDay(e.target.value)}
          >
            {[1, 2, 3, 4, 5].map((d) => (
              <option key={d} value={d}>
                Dia {d}
              </option>
            ))}
          </select>

          <select
            className="w-full p-3 rounded-xl border"
            value={target}
            onChange={(e) => setTarget(e.target.value)}
          >
            <option value="">Votar em...</option>
            {participants
              .filter((p) => p.id !== parseInt(voter))
              .map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name}
                </option>
              ))}
          </select>

          <select
            className="w-full p-3 rounded-xl border"
            value={emoji}
            onChange={(e) => setEmoji(e.target.value)}
          >
            <option value="">Escolher emoji...</option>
            {emojis.map((e) => (
              <option key={e.id} value={e.id}>
                {e.icon} {e.name}
              </option>
            ))}
          </select>

          <button
            onClick={handleVote}
            className="w-full bg-purple-600 text-white p-3 rounded-xl font-bold active:scale-95 transition"
          >
            Enviar voto 🚀
          </button>
        </div>

        {/* RANKING */}
        <div className="mt-8">
          <h2 className="text-xl font-semibold mb-3">🏆 Ranking</h2>

          <div className="space-y-2">
            {ranking.map((r, index) => (
              <div
                key={index}
                className="flex justify-between bg-gray-100 p-3 rounded-xl"
              >
                <span>
                  {index + 1}º {r.name}
                </span>
                <span className="font-bold">{r.score}</span>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}

export default App;