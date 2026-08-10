import React from "react";
import { FlatList, Image, Pressable, Text, View } from "react-native";

import icons from "../assets/icons.js";

export default function TaskListScreen({ tasks, onOpen, onAdd }) {
  return (
    <View style={styles.screen}>
      <View style={styles.header}>
        <Image source={icons.wave} style={styles.flourish} />
        <Text style={styles.title}>Today</Text>
      </View>

      <FlatList
        data={tasks}
        keyExtractor={(task) => task.id}
        renderItem={({ item }) => (
          <Pressable style={styles.row} onPress={() => onOpen(item.id)}>
            <Text style={styles.rowTitle}>{item.title}</Text>
            <Text style={styles.rowWhen}>{item.when}</Text>
          </Pressable>
        )}
      />

      <Pressable style={styles.add} onPress={onAdd}>
        <Image source={icons.plus} style={styles.addIcon} />
      </Pressable>
    </View>
  );
}

const styles = {
  screen: { flex: 1, padding: 16 },
  header: { flexDirection: "row", alignItems: "center", gap: 8 },
  flourish: { width: 28, height: 28, opacity: 0.5 },
  title: { fontSize: 28, fontWeight: "600" },
  row: { paddingVertical: 12 },
  rowTitle: { fontSize: 17 },
  rowWhen: { fontSize: 13, opacity: 0.6 },
  add: { position: "absolute", right: 24, bottom: 24, padding: 16 },
  addIcon: { width: 24, height: 24 },
};
