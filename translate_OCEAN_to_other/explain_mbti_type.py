# Функция для предоставления подробных текстовых объяснений результатов MBTI
def explain_mbti_type(mbti_type):
    explanations = {
        'INTJ': """INTJ («Архитектор»)
Основные черты: Логичен, аналитичен, уверен в себе, независим.
Преимущества: Стратегический и целеустремленный, отлично справляется с решением сложных проблем.
Мотивация: Стремление к улучшению и оптимизации процессов.
Общение: Сдержан, не любит светских бесед, но уверен и убедителен в диалоге, если считает его необходимым.
Рекомендация: Работайте над развитием эмоционального интеллекта и социальных навыков, чтобы более эффективно взаимодействовать с другими и расширять свои возможности влияния.""",

        'INTP': """INTP («Логик»)
Основные черты: Инновационен, исследовательский, погруженный в идеи, сосредоточен на логике.
Преимущества: Склонен к научной деятельности, изобретательности и решению логических головоломок.
Мотивация: Исследование, поиск смысла и структурирование идей.
Общение: Лаконичен, может показаться отстраненным, но его энтузиазм вспыхивает, если разговор затрагивает его интересы.
Рекомендация: Старайтесь уделять внимание практическому применению ваших идей и активно участвуйте в командах, чтобы ваши инновации нашли реализацию.""",

        'ENTJ': """ENTJ («Командир»)
Основные черты: Авторитетен, уверенный лидер, направленный на достижение целей.
Преимущества: Эффективен, организован, умеет мотивировать и направлять других на результат.
Мотивация: Руководство, успех, эффективность.
Общение: Напорист, стремится к эффективности в диалоге, может быть прямолинеен и даже резок.
Рекомендация: Помните о важности эмоциональных потребностей других людей и стремитесь быть более чуткими, чтобы укреплять командный дух и лояльность.""",

        'ENTP': """ENTP («Изобретатель»)
Основные черты: Оригинален, находчив, ищет новизны, склонен к интеллектуальной игре.
Преимущества: Легко генерирует идеи, адаптивен, находит нестандартные решения.
Мотивация: Исследование, решение интеллектуальных задач, проверка границ возможного.
Общение: Быстрый, харизматичный и энергичный собеседник, любит дебаты и словесные баталии.
Рекомендация: Фокусируйтесь на завершении проектов и внедрении идей, а также проявляйте терпение к более консервативным точкам зрения.""",

        'INFJ': """INFJ («Адвокат»)
Основные черты: Чувствителен, интуитивен, принципиален, имеет глубоко укорененные ценности.
Преимущества: Заботлив, хорошо понимает эмоции других, предан идеалам.
Мотивация: Помогать другим, влиять на мир позитивно.
Общение: Внимателен и доброжелателен, предпочитает глубокие и искренние беседы.
Рекомендация: Старайтесь не перегружать себя заботами о других и уделяйте время собственным потребностям, чтобы избежать эмоционального выгорания.""",

        'INFP': """INFP («Посредник»)
Основные черты: Идеалистичен, ориентирован на внутренние ценности, творческий и чувствительный.
Преимущества: Сострадателен, склонен к творчеству, эмоционально восприимчив.
Мотивация: Поиск смысла, самовыражение, помощь другим.
Общение: Мягок и открытен, предпочитает избегать конфликтов, заботится о гармонии.
Рекомендация: Развивайте навыки практической реализации своих идей и учитесь справляться с конфликтами, чтобы более эффективно достигать своих целей.""",

        'ENFJ': """ENFJ («Наставник»)
Основные черты: Теплый, заботливый, естественный лидер, вдохновляет других.
Преимущества: Способен к сильной эмпатии, поддерживает других, мотивирует на развитие.
Мотивация: Поддержка и обучение других, достижение гармонии в коллективе.
Общение: Искренний и убедительный, легко находит подход к каждому, стремится понять других.
Рекомендация: Уделяйте время собственным потребностям и границам, чтобы поддерживать баланс и избегать эмоционального истощения.""",

        'ENFP': """ENFP («Борец»)
Основные черты: Открыт, креативен, эмоционален, энергичен.
Преимущества: Воодушевляет других, часто проявляет яркую харизму, оптимистичен.
Мотивация: Исследование мира, нахождение новых идей и вдохновения.
Общение: Жизнерадостный и активный, любит общение и готов делиться идеями.
Рекомендация: Работайте над организационными навыками и фокусируйтесь на завершении проектов, чтобы ваши идеи приносили реальные результаты.""",

        'ISTJ': """ISTJ («Логист»)
Основные черты: Стабильный, надежный, склонен к деталям, традиционен.
Преимущества: Старателен, эффективен, уважает законы и порядок, лоялен.
Мотивация: Выполнение обязанностей, поддержание стабильности и порядка.
Общение: Консервативен, предпочитает конкретные темы, избегает ненужной многословности.
Рекомендация: Будьте открыты новым идеям и гибкости, это поможет адаптироваться к изменениям и расширить возможности развития.""",

        'ISFJ': """ISFJ («Защитник»)
Основные черты: Уважителен, заботлив, лоялен, ориентирован на помощь.
Преимущества: Внимателен к деталям, предан, защищает близких.
Мотивация: Поддержка других, выполнение морального долга.
Общение: Мягок и тактичен, предпочитает близкие, доверительные отношения.
Рекомендация: Не забывайте о своих собственных потребностях и учитесь говорить «нет», чтобы поддерживать баланс между помощью другим и заботой о себе.""",

        'ESTJ': """ESTJ («Администратор»)
Основные черты: Лидерский, практичный, решительный, направленный на достижение результатов.
Преимущества: Эффективен, рационален, организует работу коллектива.
Мотивация: Поддержание порядка, достижение практических результатов.
Общение: Прямой и целеустремленный, предпочитает продуктивные разговоры.
Рекомендация: Проявляйте больше гибкости и понимания к различным точкам зрения, это улучшит взаимодействие с другими и повысит эффективность работы в команде.""",

        'ESFJ': """ESFJ («Консул»)
Основные черты: Дружелюбный, тактичный, заботливый, социально ориентированный.
Преимущества: Заботлив, склонен к поддержанию порядка и традиций, привязан к людям.
Мотивация: Поддержка близких и коллектива, уважение традиций.
Общение: Открыт и общителен, любит взаимодействовать и помогать.
Рекомендация: Старайтесь принимать перемены и новые идеи с большим энтузиазмом, это поможет вам и окружающим развиваться и расти.""",

        'ISTP': """ISTP («Виртуоз»)
Основные черты: Практичный, независимый, находчивый, любит эксперименты.
Преимущества: Отличается аналитическим мышлением, мастерски справляется с техникой.
Мотивация: Решение технических задач, поиск новых путей применения знаний.
Общение: Немного замкнут, но открыт к тем, кто разделяет его интересы.
Рекомендация: Развивайте коммуникативные навыки и делитесь своими идеями с другими, это может привести к новым возможностям и сотрудничеству.""",

        'ISFP': """ISFP («Артист»)
Основные черты: Чувствительный, творческий, ориентирован на настоящее, сдержанный.
Преимущества: Склонен к искусству, эмоционален, заботится о гармонии и красоте.
Мотивация: Поиск самовыражения, наслаждение моментом.
Общение: Мягок, тактичен, предпочитает общение один на один.
Рекомендация: Старайтесь выходить из зоны комфорта и пробовать новое, это поможет раскрыть ваш потенциал и обогатит жизненный опыт.""",

        'ESTP': """ESTP («Маршал»)
Основные черты: Энергичность, практичность, решительность, смелость. ESTP склонны к авантюризму и поиску новых впечатлений.
Преимущества: Умеют быстро адаптироваться, решать проблемы в реальном времени, находить нестандартные пути. Легко находят общий язык, а также обладают хорошей интуицией в отношении людей.
Мотивация: Получение адреналина и свободы действий, преодоление вызовов и непосредственное участие в новых событиях. Им важно видеть результаты своих действий.
Общение: Общительны, любят короткие и динамичные разговоры. Прямолинейны и открыты, предпочитают говорить по делу и с юмором.
Рекомендация: Учитесь планировать наперед и обдумывать долгосрочные последствия своих действий, это поможет вам достигать больших успехов и избегать нежелательных ситуаций.""",

        'ESFP': """ESFP («Исполнитель»)
Основные черты: Дружелюбие, общительность, спонтанность, ориентированность на наслаждение жизнью. ESFP любят быть в центре внимания и привносить позитив.
Преимущества: Легко адаптируются, создают приятную атмосферу вокруг себя, находят подход к людям разных характеров. Способны вдохновлять других на активные действия.
Мотивация: Свобода, возможность наслаждаться настоящим моментом, поддержка дружеских связей и поиск новых увлекательных впечатлений.
Общение: Общительны и эмоциональны, любят обсуждать личные и интересные темы. Предпочитают разговоры, которые вызывают эмоциональный отклик и могут сближать людей.
Рекомендация: Старайтесь уделять больше внимания планированию и организации, чтобы ваши таланты приносили долгосрочные результаты и способствовали достижению целей.""",
    }

    if mbti_type in explanations:
        return explanations[mbti_type]
    else:
        return "Неправильно введен тип MBTI."