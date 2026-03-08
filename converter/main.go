package main

import (
	"encoding/csv"
	"encoding/json"
	"fmt"
	"os"
)

func main() {
	// Проверяем аргументы
	if len(os.Args) < 3 {
		fmt.Println("Использование: converter <input.json> <output.csv>")
		os.Exit(1)
	}

	inputFile := os.Args[1]
	outputFile := os.Args[2]

	// 1. Читаем JSON файл
	jsonData, err := os.ReadFile(inputFile)
	if err != nil {
		fmt.Printf("Ошибка чтения JSON: %v\n", err)
		os.Exit(1)
	}

	// 2. Парсим JSON (может быть массив или один объект)
	var data []map[string]interface{}

	// Пробуем как массив
	err = json.Unmarshal(jsonData, &data)
	if err != nil {
		// Если не массив, пробуем как один объект
		var single map[string]interface{}
		if err2 := json.Unmarshal(jsonData, &single); err2 != nil {
			fmt.Printf("Ошибка парсинга JSON: %v\n", err)
			os.Exit(1)
		}
		// Превращаем один объект в массив из одного элемента
		data = []map[string]interface{}{single}
	}

	// 3. Если данных нет
	if len(data) == 0 {
		fmt.Println("JSON не содержит данных")
		os.Exit(0)
	}

	// 4. Создаём CSV файл
	csvFile, err := os.Create(outputFile)
	if err != nil {
		fmt.Printf("Ошибка создания CSV: %v\n", err)
		os.Exit(1)
	}
	defer csvFile.Close()

	writer := csv.NewWriter(csvFile)
	defer writer.Flush()

	// 5. Получаем заголовки (ключи первого объекта)
	headers := make([]string, 0, len(data[0]))
	for key := range data[0] {
		headers = append(headers, key)
	}

	// 6. Записываем заголовки
	if err := writer.Write(headers); err != nil {
		fmt.Printf("Ошибка записи заголовков: %v\n", err)
		os.Exit(1)
	}

	// 7. Записываем данные
	for _, row := range data {
		record := make([]string, len(headers))
		for i, key := range headers {
			// Преобразуем значение в строку
			value := row[key]
			record[i] = fmt.Sprintf("%v", value)
		}
		if err := writer.Write(record); err != nil {
			fmt.Printf("Ошибка записи строки: %v\n", err)
			os.Exit(1)
		}
	}

	fmt.Printf("✅ Конвертация завершена: %s -> %s\n", inputFile, outputFile)
	fmt.Printf("📊 Обработано записей: %d\n", len(data))
}
