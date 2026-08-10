import React, { useEffect, useState } from "react";
import { SafeAreaView, Text } from "react-native";

import { createClient, createServer, openStore } from "./core/index.js";
import BookingScreen from "./screens/BookingScreen.js";
import SettingsScreen from "./screens/SettingsScreen.js";
import TaskDetailScreen from "./screens/TaskDetailScreen.js";
import TaskListScreen from "./screens/TaskListScreen.js";

const DATA_DIR = ".tern-data";

export default function App() {
  const [client] = useState(() =>
    createClient(deviceId(), openStore(DATA_DIR), createServer()));
  const [screen, setScreen] = useState("list");
  const [state, setState] = useState(() => client.state());

  useEffect(() => {
    client.flush().then(() => setState(client.state()));
  }, [client]);

  const shared = { state, client, setState, setScreen };

  return (
    <SafeAreaView style={{ flex: 1 }}>
      <Text>{client.status() === "ok" ? "" : "Syncing"}</Text>
      {screen === "list" && <TaskListScreen {...shared} />}
      {screen === "detail" && <TaskDetailScreen {...shared} />}
      {screen === "booking" && <BookingScreen {...shared} />}
      {screen === "settings" && <SettingsScreen {...shared} />}
    </SafeAreaView>
  );
}

function deviceId() {
  return "device";
}
