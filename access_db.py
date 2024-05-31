def get_content(conn, database):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * from centre_work.{database}")
    all_st = cursor.fetchall()
    cursor.close()
    return all_st


def insert_data(conn, database, column, values):
    cursor = conn.cursor()
    if database == "passportdata":
        cursor.execute(
            f"INSERT INTO centre_work.{database} ({column}) VALUES(%s, %s, %s)", values
        )
    if database == "personaldata":
        cursor.execute(
            f"INSERT INTO centre_work.{database} ({column})"
            "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            values,
        )
    if database == "vacancy":
        cursor.execute(
            f"INSERT INTO centre_work.{database} ({column})"
            "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            values,
        )
    if database == "regperson":
        cursor.execute(
            f"SELECT idreg, vacancy from centre_work.{database} WHERE id={values[0]}"
        )
        data_information = cursor.fetchall()
        if len(data_information) == 0:
            values.append("1")
            values[5] = None
            cursor.execute(
                f"INSERT INTO centre_work.{database} ({column})"
                "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                values,
            )
        else:
            last_str = data_information[-1]
            values.append(last_str[0] + 1)
            if values[5] == "None":
                values[5] = None
            cursor.execute(
                f"INSERT INTO centre_work.{database} ({column})"
                "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                values,
            )
            if values[5] is not None:
                cursor.execute(
                    f"UPDATE centre_work.vacancy SET active=false WHERE jobid={values[5]}"
                )
            else:
                cursor.execute(
                    f"UPDATE centre_work.vacancy SET active=true WHERE jobid={last_str[-1]}"
                )
    conn.commit()
    cursor.close()
