#include <SFML/Graphics.hpp>
#include <vector>

bool AABBvsAABB(const sf::FloatRect& a, const sf::FloatRect& b)
{
  return a.findIntersection(b).has_value();
}

int main()
{
  sf::RenderWindow window(sf::VideoMode({800, 600}), "TEST");
  window.setFramerateLimit(60);

  sf::Texture texture;
  if (!texture.loadFromFile("player3.png")) return -1;

  const int frameWidth = 280;
  const int frameHeight = 400;
  int cuf = 0;
  
  sf::Sprite sprite(texture);
  sprite.setTextureRect(sf::IntRect(sf::Vector2i(0, 0), sf::Vector2i(frameWidth, frameHeight)));
  sprite.setPosition({static_cast<float>(100.f), static_cast<float>(300.f)});
  sprite.setScale({0.25f, 0.25f});
  sf::Clock clock, moveclock;
  bool moving = false;

  sf::RectangleShape wall({100, 300});
  wall.setFillColor(sf::Color::Red);
  wall.setPosition({600, 150});

  bool smt = true;  

  auto a = sprite.getGlobalBounds();
  auto b = sprite.getGlobalBounds();
  float Gra = 600.f; 
  float vel = 0.f;
  float velx = 0.f;  

  sprite.setOrigin({frameWidth / 2.f, frameHeight / 2.f}); 
  while (window.isOpen()) 
  {
   while (auto event = window.pollEvent())
   {
     if (event->is<sf::Event::Closed>()) window.close();
   }
   
   if (clock.getElapsedTime().asSeconds() >= 0.1f)
   { 
     if (moving == true)
     {   
       cuf = (cuf +1) % 5;
       sprite.setTextureRect(sf::IntRect(sf::Vector2i(cuf*frameWidth, 0),sf::Vector2i(frameWidth, frameHeight)));
       clock.restart();
     }
   }
  
   float dt = moveclock.restart().asSeconds();
   sf::Vector2f movement(0.f, 0.f);   

   if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::D) && smt == true)
   {
      if (velx < 4500.f) velx += 3000.f * dt;
      sprite.setScale({0.25f, 0.25f});
      moving = true;
   }
   else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::A) && smt == true) 
   {
     if (velx > -4500.f) velx -= 3000.0f * dt;
     sprite.setScale({-0.25f, 0.25f});
     moving = true;
   }else moving = false; 
   
   if (sprite.getPosition().y < 450.f)
   {
     vel += Gra * dt;     
   }
   else { vel = 0.f; sprite.setPosition({sprite.getPosition().x , 450.f}); smt = true;}

   if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::E) && sprite.getPosition().y > 350.f && smt == true)
   {
      vel -= 400.f;
      smt = false;
   }
   if (smt == true) velx *= 0.85f; else velx *= 0.99f;
   movement.y = vel * dt;
   movement.x = velx * dt;   

   sprite.move(movement);

   a = sprite.getGlobalBounds();
   b = wall.getGlobalBounds();

   if (AABBvsAABB(a, b))
   {
     if (smt == true) sprite.move(-movement); else
     { 
        auto su = movement;
        su.y = 0.f;
        sprite.move(-su);
     } 
   }

   window.clear(sf::Color::White);
   window.draw(sprite); 
   window.draw(wall);
   window.display();
  }
  
  return 0;
}
