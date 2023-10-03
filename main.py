from fastapi import FastAPI
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



app=FastAPI()

#cargamos nuestros archivos
df_reviews = pd.DataFrame(pd.read_csv(r"src/reviews.csv",sep='|'))
df_games = pd.DataFrame(pd.read_csv(r"src/steam_games.csv",sep='|'))
df_items = pd.DataFrame(pd.read_csv(r"src/items.csv",sep='|'))
df_ml=pd.DataFrame(pd.read_csv(r"src/reviews_nosentiment.csv",sep="|"))

#realizamos los merge necesarios para las funciones
df_item_games=pd.merge(df_items,df_games, left_on="item_id",right_on="id")[["user_id","genres","release_date","playtime_forever"]]
df_reviews_games=pd.merge(df_reviews,df_games,left_on="item_id",right_on="id")[["user_id","release_date","recommend","sentiment_analysis","item_id","app_name"]]

#Definimos ruta para la raiz de la aplicación
@app.get("/")
async def root():
    return {"Mensaje": "¡Bienvenido a mi aplicacion de FastAPI!"}

#La siguiente funcion regresa el año que mas horas de juego acumuló, tiene parametro de entrada un string con el genero a revisar.
@app.get("/playtime_genre/{genero}")
def PlayTimeGenre(genero:str):
    #hacemos el filtro por genero
    filter = df_item_games[df_item_games["genres"].str.lower().str.contains(genero.strip().lower())]
    #agrupamos por año y sumamos las horas totales de juego
    year=filter.groupby("release_date").sum("playtime_forever").sort_values(by="playtime_forever",ascending=False).reset_index()
    #damos formato a la salida

    if year.empty:
        return {"Favor de revisar la escritura de su elección "+ str(genero.title()+" ,el género tiene que estar escrito en ingles ej: action, indie, simulation")}
    else:
        return {"Año de lanzamiento con más horas jugadas para '"+str(genero).title()+"' es":int(year.iloc[0]["release_date"])}

#Devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
@app.get("/user_for_genre/{genero}")
def UserForGenre(genero: str):
    # Hacemos filtro del genero
    filter = df_item_games[df_item_games["genres"].str.lower().str.contains(genero.strip().lower())]
    
    #Mensaje en caso de error al teclear el género
    if filter.empty:
        return {"Mensaje": f"No hay datos para el género: {genero.title()}"}
    
    # Con el filtro anterior, buscamos al usuario que más horas acumuló de este género
    filter_user = (filter.groupby(by=["user_id", "genres"]).sum("playtime_forever")
                   .sort_values(by="playtime_forever", ascending=False).reset_index()).iloc[0]["user_id"]
    
    # Creamos una lista con los años y las horas de juego
    user_filter = filter[filter["user_id"] == filter_user]
    
    years = user_filter.groupby("release_date").sum("playtime_forever").reset_index()
    years_list = [{"Año": row["release_date"], "Horas": int(row["playtime_forever"])} for _, row in years.iterrows()]
    
    # Damos formato a la salida
    return {f"Usuario con más horas jugadas para {genero.title()}": filter_user, "horas jugadas": years_list}

#Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado.
@app.get("/Users_Recommend/{int}")
def UsersRecommend(anio: int):
    # Filtramos año, recomendado por usuarios como verdadero y el sentimiento positivo y neutral
    filtered = df_reviews_games[(df_reviews_games["release_date"] == anio) & (df_reviews_games["recommend"] == True) & ((df_reviews_games["sentiment_analysis"] == 1) | (df_reviews_games["sentiment_analysis"] == 2))]
    
    # revisamos si tenemos juegos recomendados
    if filtered.empty:
        return "No existen juegos recomendados para este año, pruebe con otra fecha por favor"
    
    # Contamos cuantas reseñas positivas y neutrales tenemos
    grouped_counts = filtered.groupby("app_name")["sentiment_analysis"].value_counts().unstack(fill_value=0).reset_index()
    
    # Sumamos los sentimientos neutrales y positivos, se pone la columna de la suma de estos parametros
    grouped_counts['Total Sentiment Count'] = grouped_counts.get(1, 0) + grouped_counts.get(2, 0)
    
    # Obtenemos el top 3 o menos
    sorted_counts = grouped_counts.sort_values(by='Total Sentiment Count', ascending=False)
    
    # Determinamos el numero de lugares
    num_games = min(3, len(sorted_counts))
    
    # Creamos una lsita de diccionarios con los lugares ganadores.
    list_top_games = [{"Puesto " + str(index + 1): app_name} for index, app_name in enumerate(sorted_counts["app_name"][:num_games])]
    
    return list_top_games


#Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado.
@app.get("/Users_Not_Recommend/{int}")
def UsersNotRecommend( anio : int ): #Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)
    # Filtramos año, no recomendado por usuarios como verdadero y el sentimiento negativo
    filtered = df_reviews_games[(df_reviews_games["release_date"] == anio) & (df_reviews_games["recommend"] == False) & ((df_reviews_games["sentiment_analysis"] == 0))]
    
    # revisamos si tenemos juegos recomendados
    if filtered.empty:
        return "No existen juegos no recomendados para este año, pruebe con otra fecha por favor"
    
    # agrupamos
    grouped_counts = filtered.groupby("app_name")["sentiment_analysis"].value_counts().unstack(fill_value=0).reset_index()
    
    #contamos los sentimientos negativos
    grouped_counts['Total Sentiment Count'] = grouped_counts.get(0)
    
    # Obtenemos el top 3 o menos
    sorted_counts = grouped_counts.sort_values(by='Total Sentiment Count', ascending=False)
    
    # Determinamos el numero de lugares
    num_games = min(3, len(sorted_counts))
    
    # Creamos una lsita de diccionarios con los lugares ganadores.
    list_top_games = [{"Puesto " + str(index + 1): app_name} for index, app_name in enumerate(sorted_counts["app_name"][:num_games])]
    
    return list_top_games

#Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.
@app.get("/Sentiment_Analysis/{int}")
def sentiment_analysis(anio:int):
    filter=df_reviews_games[(df_reviews_games["release_date"] == anio)]
    if filter.empty:
        return {"No existen juegos no recomendados para este año, pruebe con otra fecha por favor"}
    grouped= filter.groupby("app_name")["sentiment_analysis"].value_counts().unstack(fill_value=0).reset_index()
    return {"Negative = "+str(grouped[0].sum()),"Neutral = "+str(grouped[1].sum()),"Positive = "+str(grouped[2].sum())}

@app.get("/Recomendacion_Usuario/{str}")
def get_recommendations(user_id:str):
    num_recommendations=5
    # Filtrar las reseñas del usuario específico
    user_reviews = df_ml[df_ml['user_id'] == user_id]['review'].tolist()

    # Inicializar el vectorizador TF-IDF
    tfidf_vectorizer = TfidfVectorizer()

    # Calcular la matriz TF-IDF para las reseñas del usuario
    tfidf_matrix = tfidf_vectorizer.fit_transform(user_reviews)

    # Calcular la similitud de coseno entre todas las reseñas del usuario
    cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Obtener las reseñas más similares a las del usuario actual
    similar_indices = cosine_similarities.argsort()[:, ::-1]  # Ordenar en orden descendente

    # Obtener las recomendaciones basadas en similitud
    recommendations = []
    seen_item_ids = set(df_ml[df_ml['user_id'] == user_id]['item_id'].tolist())

    for idx in similar_indices[0]:
        item_id = df_ml.iloc[idx]['item_id']
        if item_id not in seen_item_ids:
            recommendations.append(int(item_id))
            seen_item_ids.add(item_id)
            if len(recommendations) >= num_recommendations:
                break

    return recommendations