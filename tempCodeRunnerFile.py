r ix in records], indent=2 )
  
    return jsonify(data_json_form)

if __name__ == "__main__":
    app.run(host='0.0.0.0')