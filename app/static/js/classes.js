export class Colaborador {
    constructor(id, name, email, password) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.password = password;
    }
}
export class Catalogo {
    constructor(id, title, content, creation_date, image_id) {
        this.id = id;
        this.title = title;
        this.content = content;
        this.creation_date = creation_date;
        this.image_id = image_id;
    }
}