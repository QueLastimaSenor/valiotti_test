select city from city_population
where population = (
    select min(population)
    from city_population
)